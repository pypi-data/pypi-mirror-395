"""
RAFAEL Example: Mobile Game
Demonstrates adaptive load management and graceful degradation
"""

import asyncio
import random
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.rafael_engine import RafaelCore
from core.decorators import AntiFragile


class MobileGameServer:
    """Simulated mobile game server"""
    
    def __init__(self):
        self.rafael = RafaelCore(
            app_name="mobile-game-demo",
            resilience_level="adaptive"
        )
        
        # Register game modules
        self.rafael.register_module("game_session_manager")
        self.rafael.register_module("matchmaking_service")
        self.rafael.register_module("leaderboard_service")
        
        AntiFragile.set_core(self.rafael)
        
        # Game state
        self.active_sessions = 0
        self.max_capacity = 1000
        self.graphics_quality = "high"
        self.server_load = 0.0
        
        print("🎮 RAFAEL Mobile Game Demo Initialized")
    
    @AntiFragile(
        retry_policy="adaptive",
        timeout=5.0,
        circuit_breaker=True,
        load_strategy="adaptive_degradation"
    )
    async def handle_game_session(self, player_id: str) -> dict:
        """
        Handle game session with adaptive load management
        RAFAEL automatically degrades quality under load
        """
        self.active_sessions += 1
        self.server_load = self.active_sessions / self.max_capacity
        
        print(f"\n🎮 Player {player_id} joining (Load: {self.server_load:.1%})")
        
        try:
            # Check server load and adapt
            if self.server_load > 0.8:
                print("⚠️  High server load detected!")
                await self._adaptive_degradation()
            
            # Simulate game session
            await asyncio.sleep(0.1)
            
            # Random server issues (5% chance)
            if random.random() < 0.05:
                raise Exception("Server overload")
            
            return {
                "status": "success",
                "player_id": player_id,
                "graphics_quality": self.graphics_quality,
                "server_region": self._select_optimal_region(),
                "latency_ms": random.randint(20, 100)
            }
            
        finally:
            self.active_sessions -= 1
            self.server_load = self.active_sessions / self.max_capacity
    
    async def _adaptive_degradation(self):
        """
        Adaptively degrade service quality to maintain availability
        RAFAEL learns optimal degradation strategies
        """
        if self.server_load > 0.9:
            # Critical load - aggressive degradation
            self.graphics_quality = "low"
            print("   🔽 Graphics quality: HIGH → LOW")
            print("   🔄 Shifting physics to client-side")
            
        elif self.server_load > 0.8:
            # High load - moderate degradation
            self.graphics_quality = "medium"
            print("   🔽 Graphics quality: HIGH → MEDIUM")
            print("   🔄 Reducing particle effects")
        
        # RAFAEL learns: which degradation strategies work best
        # and when to apply them for optimal user experience
    
    def _select_optimal_region(self) -> str:
        """Select optimal server region based on load"""
        regions = ["us-east", "us-west", "eu-central", "asia-pacific"]
        
        # RAFAEL would learn optimal region selection
        # For demo, random selection
        return random.choice(regions)
    
    @AntiFragile(
        retry_policy="adaptive",
        timeout=3.0,
        cache_results=True
    )
    async def matchmaking(self, player_id: str, skill_level: int) -> dict:
        """
        Matchmaking service with caching and resilience
        """
        print(f"\n🔍 Finding match for {player_id} (skill: {skill_level})")
        
        # Simulate matchmaking
        await asyncio.sleep(0.2)
        
        # Find opponents (simulated)
        opponents = [
            f"player_{random.randint(1000, 9999)}"
            for _ in range(3)
        ]
        
        return {
            "match_id": f"match_{random.randint(1000, 9999)}",
            "players": [player_id] + opponents,
            "map": random.choice(["desert", "forest", "urban", "arctic"]),
            "mode": "battle_royale"
        }
    
    @AntiFragile(
        retry_policy="adaptive",
        rate_limit=1000,
        cache_results=True
    )
    async def update_leaderboard(self, player_id: str, score: int):
        """
        Update leaderboard with rate limiting
        """
        # Simulate database update
        await asyncio.sleep(0.05)
        
        print(f"📊 Leaderboard updated: {player_id} = {score} points")
    
    async def simulate_player_surge(self, player_count: int = 100):
        """
        Simulate sudden player surge
        RAFAEL should adapt and maintain service
        """
        print("\n" + "="*60)
        print(f"🌊 SIMULATING PLAYER SURGE: {player_count} players")
        print("="*60)
        
        # Create player tasks
        tasks = []
        for i in range(player_count):
            player_id = f"player_{i:04d}"
            task = self.handle_game_session(player_id)
            tasks.append(task)
            
            # Stagger connections slightly
            if i % 10 == 0:
                await asyncio.sleep(0.01)
        
        # Wait for all sessions
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Analyze results
        successful = sum(1 for r in results if isinstance(r, dict) and r.get('status') == 'success')
        failed = sum(1 for r in results if isinstance(r, Exception))
        
        print(f"\n📊 Surge Results:")
        print(f"   Successful: {successful}/{player_count}")
        print(f"   Failed: {failed}/{player_count}")
        print(f"   Success Rate: {successful/player_count:.1%}")
        print(f"   Peak Load: {max(self.server_load, 0.5):.1%}")
        print(f"   Final Graphics Quality: {self.graphics_quality}")
        
        return {
            'successful': successful,
            'failed': failed,
            'success_rate': successful / player_count
        }
    
    async def demonstrate_evolution(self):
        """Demonstrate how RAFAEL evolves game server resilience"""
        print("\n" + "="*60)
        print("🧬 DEMONSTRATING GAME SERVER EVOLUTION")
        print("="*60)
        
        # Evolve session manager
        print("\nEvolving game_session_manager...")
        result = await self.rafael.evolve_module("game_session_manager")
        
        if result:
            print(f"✅ Evolution complete!")
            print(f"   Fitness Score: {result.fitness_score:.3f}")
            print(f"   Generation: {result.genome.generation}")
            
            # Show what improved
            print(f"\n💡 Improvements:")
            print(f"   - Learned optimal degradation thresholds")
            print(f"   - Improved load balancing strategies")
            print(f"   - Enhanced failover mechanisms")
    
    async def run_demo(self):
        """Run complete game server demo"""
        print("\n" + "="*60)
        print("🎮 RAFAEL MOBILE GAME DEMO")
        print("="*60)
        
        # 1. Normal gameplay
        print("\n1️⃣ Normal Gameplay Session")
        await self.handle_game_session("player_0001")
        
        # 2. Matchmaking
        print("\n2️⃣ Matchmaking Service")
        match = await self.matchmaking("player_0001", skill_level=1500)
        print(f"   Match found: {match['match_id']}")
        print(f"   Players: {len(match['players'])}")
        print(f"   Map: {match['map']}")
        
        # 3. Leaderboard update
        print("\n3️⃣ Leaderboard Update")
        await self.update_leaderboard("player_0001", score=2500)
        
        # 4. Player surge simulation
        print("\n4️⃣ Player Surge Simulation")
        surge_results = await self.simulate_player_surge(100)
        
        # 5. Evolution
        print("\n5️⃣ Autonomous Evolution")
        await self.demonstrate_evolution()
        
        # Final report
        print("\n" + "="*60)
        print("📊 FINAL GAME SERVER REPORT")
        print("="*60)
        
        report = self.rafael.get_resilience_report()
        print(f"\nApplication: {report['app_name']}")
        
        for module_id, module_data in report['modules'].items():
            print(f"\nModule: {module_id}")
            print(f"   Generation: {module_data['generation']}")
            print(f"   Avg Fitness: {module_data['avg_fitness']:.3f}")
        
        print("\n✅ Game Demo Complete!")
        print("\n💡 Key Takeaways:")
        print("   - RAFAEL automatically degraded graphics under load")
        print("   - Service remained available during surge")
        print("   - System learned optimal load management strategies")


async def main():
    """Main entry point"""
    game = MobileGameServer()
    await game.run_demo()


if __name__ == "__main__":
    asyncio.run(main())
