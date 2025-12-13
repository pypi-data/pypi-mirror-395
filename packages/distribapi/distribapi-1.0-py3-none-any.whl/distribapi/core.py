import time
import psutil
import asyncio
import aiohttp
from typing import List, Dict, Callable, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ResourceType(Enum):
    CPU = "cpu"
    RAM = "ram"
    GPU = "gpu"


@dataclass
class Endpoint:
    url: str
    name: str
    priority: int = 1
    max_cpu: float = 80.0
    max_ram: float = 80.0
    max_gpu: float = 80.0
    timeout: float = 30.0
    
    def __post_init__(self):
        self.avg_latency: float = 0.0
        self.request_count: int = 0
        self.failed_requests: int = 0


class DistribAPI:
    # Main class
    
    def __init__(self):
        self.endpoints: List[Endpoint] = []
        self.local_handler: Optional[Callable] = None
        self.monitor_resources: List[ResourceType] = []
        self.monitor_latency: bool = False
        self.fallback_local: bool = True
        self._initialized = False
        
    def init(self, 
             resources: Optional[List[str]] = None,
             latency: bool = True,
             fallback_local: bool = True):
        # Initialise the system
        if resources:
            self.monitor_resources = [
                ResourceType(r.lower()) for r in resources
            ]
        else:
            self.monitor_resources = [ResourceType.CPU, ResourceType.RAM]
            
        self.monitor_latency = latency
        self.fallback_local = fallback_local
        self._initialized = True
        print(f"distribAPI initialized - Monitoring: {[r.value.upper() for r in self.monitor_resources]}, Latency: {latency}")
    
    def add_endpoint(self, 
                     url: str, 
                     name: str,
                     priority: int = 1,
                     max_cpu: float = 80.0,
                     max_ram: float = 80.0,
                     max_gpu: float = 80.0,
                     timeout: float = 30.0):
        # Add endpoints
        endpoint = Endpoint(
            url=url,
            name=name,
            priority=priority,
            max_cpu=max_cpu,
            max_ram=max_ram,
            max_gpu=max_gpu,
            timeout=timeout
        )
        self.endpoints.append(endpoint)
        print(f"Added endpoint: {name} ({url})")
    
    def set_local_handler(self, handler: Callable):
        # Local processing initialisation
        self.local_handler = handler
        print("Local handler configured")
    
    def _get_system_resources(self) -> Dict[str, float]:
        # Get resource usage
        resources = {}
        
        if ResourceType.CPU in self.monitor_resources:
            resources['cpu'] = psutil.cpu_percent(interval=0.1)
        
        if ResourceType.RAM in self.monitor_resources:
            resources['ram'] = psutil.virtual_memory().percent
        
        if ResourceType.GPU in self.monitor_resources:
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    resources['gpu'] = sum(g.load * 100 for g in gpus) / len(gpus)
                else:
                    resources['gpu'] = 0.0
            except ImportError:
                resources['gpu'] = 0.0
        
        return resources
    
    def _score_endpoint(self, endpoint: Endpoint, current_resources: Dict[str, float]) -> float:
        # Score system for finding suitable destination
        score = 0.0
        
        for resource_type in self.monitor_resources:
            resource_key = resource_type.value
            if resource_key in current_resources:
                usage = current_resources[resource_key]
                max_val = getattr(endpoint, f'max_{resource_key}')
                
                if usage > max_val:
                    score += 1000
                else:
                    score += usage
        
        if self.monitor_latency and endpoint.avg_latency > 0:
            score += endpoint.avg_latency * 10
        
        if endpoint.request_count > 0:
            failure_rate = endpoint.failed_requests / endpoint.request_count
            score += failure_rate * 100
        
        score += endpoint.priority * 10
        
        return score
    
    def _select_endpoint(self) -> Optional[Endpoint]:
        # Selection based on score
        if not self.endpoints:
            return None
        
        current_resources = self._get_system_resources()
        
        scored = [
            (self._score_endpoint(ep, current_resources), ep)
            for ep in self.endpoints
        ]
        
        scored.sort(key=lambda x: x[0])
        
        return scored[0][1] if scored else None
    
    def _should_process_locally(self) -> bool:
        # Check if local processing is needed
        if not self.local_handler:
            return False
        
        resources = self._get_system_resources()
        
        for resource_type in self.monitor_resources:
            resource_key = resource_type.value
            if resource_key in resources:
                if resources[resource_key] > 70.0:
                    return False
        
        return True
    
    async def _forward_request(self, 
                               endpoint: Endpoint, 
                               data: Any,
                               method: str = "POST") -> Dict[str, Any]:
        # Forwarding requests
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method,
                    endpoint.url,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=endpoint.timeout)
                ) as response:
                    result = await response.json()
                    latency = time.time() - start_time
                    
                    endpoint.request_count += 1
                    endpoint.avg_latency = (
                        (endpoint.avg_latency * (endpoint.request_count - 1) + latency)
                        / endpoint.request_count
                    )
                    
                    return {
                        'success': True,
                        'data': result,
                        'endpoint': endpoint.name,
                        'latency': latency
                    }
        except Exception as e:
            endpoint.failed_requests += 1
            endpoint.request_count += 1
            return {
                'success': False,
                'error': str(e),
                'endpoint': endpoint.name
            }
    
    async def process(self, data: Any, method: str = "POST") -> Dict[str, Any]:
        # Route the things to correct destination
        if not self._initialized:
            raise RuntimeError("distribAPI not initialized. Call init() first.")
        
        if self._should_process_locally():
            try:
                result = await self.local_handler(data)
                return {
                    'success': True,
                    'data': result,
                    'endpoint': 'local',
                    'latency': 0.0
                }
            except Exception as e:
                if not self.fallback_local:
                    return {'success': False, 'error': str(e), 'endpoint': 'local'}
        
        for attempt in range(3):
            endpoint = self._select_endpoint()
            
            if not endpoint:
                break
            
            result = await self._forward_request(endpoint, data, method)
            
            if result['success']:
                return result
            
            if attempt < 2:
                await asyncio.sleep(0.5)
        
        if self.fallback_local and self.local_handler:
            try:
                result = await self.local_handler(data)
                return {
                    'success': True,
                    'data': result,
                    'endpoint': 'local_fallback',
                    'latency': 0.0
                }
            except Exception as e:
                return {'success': False, 'error': str(e), 'endpoint': 'local_fallback'}
        
        return {'success': False, 'error': 'All endpoints failed and no local handler'}
    
    def get_stats(self) -> Dict[str, Any]:
        # Get statistics
        return {
            'endpoints': [
                {
                    'name': ep.name,
                    'url': ep.url,
                    'avg_latency': round(ep.avg_latency, 3),
                    'request_count': ep.request_count,
                    'failed_requests': ep.failed_requests,
                    'success_rate': round(
                        (ep.request_count - ep.failed_requests) / ep.request_count * 100, 2
                    ) if ep.request_count > 0 else 0.0
                }
                for ep in self.endpoints
            ],
            'system_resources': self._get_system_resources()
        }
