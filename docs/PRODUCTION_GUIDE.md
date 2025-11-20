# JanusGraph Production Deployment Guide (Cassandra + Elasticsearch)

This guide gives a step-by-step checklist and recommendations for running JanusGraph in production with Cassandra as storage and Elasticsearch as mixed index.

## High-level architecture
- Cassandra cluster (multi-node, replication across racks / DCs)
- Elasticsearch cluster (separate set of nodes)
- JanusGraph servers or Gremlin Server instances (stateless application servers)
- Monitoring & backup systems

## Cassandra recommendations
- Use a 3+ node cluster for production (minimum 3 for replication).
- Replication: use NetworkTopologyStrategy and specify replication factors per data center.
- JVM: tune heap (recommendation: leave headroom, for Cassandra don't set heap above ~12-16GB without tuning).
- compaction: use LeveledCompactionStrategy for read-heavy workloads or SizeTiered for write-heavy; tune per workload.
- configure gc, disk I/O, and monitoring (nodetool, metrics).
- backups: use `nodetool snapshot` and stream snapshots off-node regularly.

## JanusGraph configuration tips
- Use a dedicated JanusGraph properties file per environment.
- Set `storage.batch-loading=true` for bulk loading operations; otherwise false for normal ops.
- Tune `storage.read/write-timeout` based on network latency.
- Use composite indexes for equality and mixed indexes for text/range queries.

## Elasticsearch recommendations
- Run Elasticsearch in its own cluster; match JanusGraph-tested versions (see compatibility).
- Set `index.number_of_replicas` and `shards` based on data size and query patterns.
- Enable snapshots to an object store (S3) for backups.
- Monitor index refresh interval for write-heavy workloads (increase interval during bulk loads).

## Monitoring & Alerting
- Collect metrics: JanusGraph JVM (JMX), Gremlin Server threads, Cassandra metrics (nodetool/metrics), Elasticsearch stats.
- Centralize logs and set alerts for node down, GC pauses, queue sizes, and high latency.

## Backup & Recovery
- Cassandra: regular snapshots + incremental backups (depending on Cassandra version).
- Elasticsearch: use snapshots API to store indices in remote repository (S3).
- Test recovery procedures in staging.

## Security & Networking
- Use VPCs/subnets and firewall rules; restrict access to ports (Cassandra 9042, ES 9200, Gremlin 8182).
- Enable TLS between components where supported.
- Use authentication and role-based access for ES and Cassandra in production.

## Capacity planning
- Benchmark with representative workloads.
- Monitor storage growth (Cassandra SSTables + ES indices).
- Plan for compaction and repair windows.

For more details consult the official JanusGraph docs and Cassandra/Elasticsearch production guides.
