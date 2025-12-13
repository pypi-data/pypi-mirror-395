"""
RAFAEL Persistence Layer
Handles saving and loading of genome state, evolution history, and metrics
"""

import json
import sqlite3
import pickle
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger("RAFAEL.Persistence")


class GenomePersistence:
    """
    Persistence layer for Adaptive Resilience Genomes
    Supports SQLite and JSON file storage
    """
    
    def __init__(self, storage_path: str = "./rafael_data", storage_type: str = "sqlite"):
        """
        Initialize persistence layer
        
        Args:
            storage_path: Path to storage directory
            storage_type: Type of storage ('sqlite' or 'json')
        """
        self.storage_path = Path(storage_path)
        self.storage_type = storage_type
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        if storage_type == "sqlite":
            self.db_path = self.storage_path / "rafael.db"
            self._init_database()
        
        logger.info(f"Persistence initialized: {storage_type} at {storage_path}")
    
    def _init_database(self):
        """Initialize SQLite database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Genomes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS genomes (
                module_id TEXT PRIMARY KEY,
                generation INTEGER,
                genes_data TEXT,
                created_at TEXT,
                updated_at TEXT,
                metadata TEXT
            )
        ''')
        
        # Evolution history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evolution_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id TEXT,
                generation INTEGER,
                fitness_score REAL,
                mutation_type TEXT,
                adopted BOOLEAN,
                timestamp TEXT,
                details TEXT,
                FOREIGN KEY (module_id) REFERENCES genomes(module_id)
            )
        ''')
        
        # Metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id TEXT,
                metric_name TEXT,
                metric_value REAL,
                timestamp TEXT,
                FOREIGN KEY (module_id) REFERENCES genomes(module_id)
            )
        ''')
        
        # Snapshots table for point-in-time recovery
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_name TEXT UNIQUE,
                snapshot_data TEXT,
                created_at TEXT,
                description TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Database schema initialized")
    
    def save_genome(self, module_id: str, genome_data: Dict[str, Any]) -> bool:
        """
        Save genome state
        
        Args:
            module_id: Module identifier
            genome_data: Genome data to save
            
        Returns:
            Success status
        """
        try:
            if self.storage_type == "sqlite":
                return self._save_genome_sqlite(module_id, genome_data)
            else:
                return self._save_genome_json(module_id, genome_data)
        except Exception as e:
            logger.error(f"Failed to save genome {module_id}: {e}")
            return False
    
    def _save_genome_sqlite(self, module_id: str, genome_data: Dict[str, Any]) -> bool:
        """Save genome to SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        genes_json = json.dumps(genome_data.get('genes', []))
        metadata_json = json.dumps(genome_data.get('metadata', {}))
        
        cursor.execute('''
            INSERT OR REPLACE INTO genomes 
            (module_id, generation, genes_data, created_at, updated_at, metadata)
            VALUES (?, ?, ?, 
                    COALESCE((SELECT created_at FROM genomes WHERE module_id = ?), ?),
                    ?, ?)
        ''', (
            module_id,
            genome_data.get('generation', 0),
            genes_json,
            module_id,
            now,
            now,
            metadata_json
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Genome saved: {module_id} (generation {genome_data.get('generation', 0)})")
        return True
    
    def _save_genome_json(self, module_id: str, genome_data: Dict[str, Any]) -> bool:
        """Save genome to JSON file"""
        file_path = self.storage_path / f"{module_id}.json"
        
        data = {
            "module_id": module_id,
            "genome": genome_data,
            "updated_at": datetime.now().isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Genome saved to JSON: {module_id}")
        return True
    
    def load_genome(self, module_id: str) -> Optional[Dict[str, Any]]:
        """
        Load genome state
        
        Args:
            module_id: Module identifier
            
        Returns:
            Genome data or None if not found
        """
        try:
            if self.storage_type == "sqlite":
                return self._load_genome_sqlite(module_id)
            else:
                return self._load_genome_json(module_id)
        except Exception as e:
            logger.error(f"Failed to load genome {module_id}: {e}")
            return None
    
    def _load_genome_sqlite(self, module_id: str) -> Optional[Dict[str, Any]]:
        """Load genome from SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT generation, genes_data, created_at, updated_at, metadata
            FROM genomes WHERE module_id = ?
        ''', (module_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            "module_id": module_id,
            "generation": row[0],
            "genes": json.loads(row[1]),
            "created_at": row[2],
            "updated_at": row[3],
            "metadata": json.loads(row[4])
        }
    
    def _load_genome_json(self, module_id: str) -> Optional[Dict[str, Any]]:
        """Load genome from JSON file"""
        file_path = self.storage_path / f"{module_id}.json"
        
        if not file_path.exists():
            return None
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return data.get("genome")
    
    def save_evolution_event(
        self,
        module_id: str,
        generation: int,
        fitness_score: float,
        mutation_type: str,
        adopted: bool,
        details: Dict[str, Any]
    ) -> bool:
        """
        Save evolution event to history
        
        Args:
            module_id: Module identifier
            generation: Generation number
            fitness_score: Fitness score achieved
            mutation_type: Type of mutation
            adopted: Whether mutation was adopted
            details: Additional details
            
        Returns:
            Success status
        """
        if self.storage_type != "sqlite":
            return True  # JSON mode doesn't track history
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO evolution_history
                (module_id, generation, fitness_score, mutation_type, adopted, timestamp, details)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                module_id,
                generation,
                fitness_score,
                mutation_type,
                adopted,
                datetime.now().isoformat(),
                json.dumps(details)
            ))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            logger.error(f"Failed to save evolution event: {e}")
            return False
    
    def get_evolution_history(
        self,
        module_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get evolution history for a module
        
        Args:
            module_id: Module identifier
            limit: Maximum number of records
            
        Returns:
            List of evolution events
        """
        if self.storage_type != "sqlite":
            return []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT generation, fitness_score, mutation_type, adopted, timestamp, details
                FROM evolution_history
                WHERE module_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (module_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "generation": row[0],
                    "fitness_score": row[1],
                    "mutation_type": row[2],
                    "adopted": bool(row[3]),
                    "timestamp": row[4],
                    "details": json.loads(row[5])
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Failed to get evolution history: {e}")
            return []
    
    def save_metric(
        self,
        module_id: str,
        metric_name: str,
        metric_value: float
    ) -> bool:
        """
        Save a metric value
        
        Args:
            module_id: Module identifier
            metric_name: Name of metric
            metric_value: Metric value
            
        Returns:
            Success status
        """
        if self.storage_type != "sqlite":
            return True
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO metrics (module_id, metric_name, metric_value, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (module_id, metric_name, metric_value, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            logger.error(f"Failed to save metric: {e}")
            return False
    
    def get_metrics(
        self,
        module_id: str,
        metric_name: Optional[str] = None,
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Get metrics for a module
        
        Args:
            module_id: Module identifier
            metric_name: Optional metric name filter
            limit: Maximum number of records
            
        Returns:
            List of metrics
        """
        if self.storage_type != "sqlite":
            return []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if metric_name:
                cursor.execute('''
                    SELECT metric_name, metric_value, timestamp
                    FROM metrics
                    WHERE module_id = ? AND metric_name = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (module_id, metric_name, limit))
            else:
                cursor.execute('''
                    SELECT metric_name, metric_value, timestamp
                    FROM metrics
                    WHERE module_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (module_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "metric_name": row[0],
                    "metric_value": row[1],
                    "timestamp": row[2]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            return []
    
    def create_snapshot(
        self,
        snapshot_name: str,
        description: str = ""
    ) -> bool:
        """
        Create a snapshot of all genomes
        
        Args:
            snapshot_name: Name for the snapshot
            description: Optional description
            
        Returns:
            Success status
        """
        if self.storage_type != "sqlite":
            logger.warning("Snapshots only supported in SQLite mode")
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all genomes
            cursor.execute('SELECT * FROM genomes')
            genomes = cursor.fetchall()
            
            snapshot_data = {
                "genomes": [
                    {
                        "module_id": row[0],
                        "generation": row[1],
                        "genes_data": row[2],
                        "created_at": row[3],
                        "updated_at": row[4],
                        "metadata": row[5]
                    }
                    for row in genomes
                ],
                "timestamp": datetime.now().isoformat()
            }
            
            cursor.execute('''
                INSERT INTO snapshots (snapshot_name, snapshot_data, created_at, description)
                VALUES (?, ?, ?, ?)
            ''', (
                snapshot_name,
                json.dumps(snapshot_data),
                datetime.now().isoformat(),
                description
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Snapshot created: {snapshot_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create snapshot: {e}")
            return False
    
    def restore_snapshot(self, snapshot_name: str) -> bool:
        """
        Restore genomes from a snapshot
        
        Args:
            snapshot_name: Name of snapshot to restore
            
        Returns:
            Success status
        """
        if self.storage_type != "sqlite":
            logger.warning("Snapshots only supported in SQLite mode")
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT snapshot_data FROM snapshots WHERE snapshot_name = ?
            ''', (snapshot_name,))
            
            row = cursor.fetchone()
            if not row:
                logger.error(f"Snapshot not found: {snapshot_name}")
                return False
            
            snapshot_data = json.loads(row[0])
            
            # Restore genomes
            for genome in snapshot_data["genomes"]:
                cursor.execute('''
                    INSERT OR REPLACE INTO genomes
                    (module_id, generation, genes_data, created_at, updated_at, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    genome["module_id"],
                    genome["generation"],
                    genome["genes_data"],
                    genome["created_at"],
                    genome["updated_at"],
                    genome["metadata"]
                ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Snapshot restored: {snapshot_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore snapshot: {e}")
            return False
    
    def list_snapshots(self) -> List[Dict[str, Any]]:
        """
        List all available snapshots
        
        Returns:
            List of snapshot info
        """
        if self.storage_type != "sqlite":
            return []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT snapshot_name, created_at, description
                FROM snapshots
                ORDER BY created_at DESC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "name": row[0],
                    "created_at": row[1],
                    "description": row[2]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Failed to list snapshots: {e}")
            return []
    
    def cleanup_old_data(self, days: int = 30) -> bool:
        """
        Clean up old metrics and history data
        
        Args:
            days: Keep data newer than this many days
            
        Returns:
            Success status
        """
        if self.storage_type != "sqlite":
            return True
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now().replace(day=datetime.now().day - days).isoformat()
            
            cursor.execute('''
                DELETE FROM metrics WHERE timestamp < ?
            ''', (cutoff_date,))
            
            cursor.execute('''
                DELETE FROM evolution_history WHERE timestamp < ?
            ''', (cutoff_date,))
            
            deleted_metrics = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            logger.info(f"Cleaned up data older than {days} days")
            return True
        except Exception as e:
            logger.error(f"Failed to cleanup old data: {e}")
            return False
    
    def export_data(self, output_path: str) -> bool:
        """
        Export all data to JSON file
        
        Args:
            output_path: Path to output file
            
        Returns:
            Success status
        """
        try:
            if self.storage_type == "sqlite":
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Export all tables
                data = {}
                
                for table in ['genomes', 'evolution_history', 'metrics', 'snapshots']:
                    cursor.execute(f'SELECT * FROM {table}')
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    
                    data[table] = [
                        dict(zip(columns, row))
                        for row in rows
                    ]
                
                conn.close()
            else:
                # Export JSON files
                data = {}
                for json_file in self.storage_path.glob("*.json"):
                    with open(json_file, 'r') as f:
                        data[json_file.stem] = json.load(f)
            
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Data exported to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export data: {e}")
            return False
