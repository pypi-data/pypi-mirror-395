import logging

from opensearchpy import OpenSearch
from mysql.connector import pooling
import yaml
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SubscriberProfileLoader:
    logger = logging.getLogger(__name__)

    def __init__(self, analytics_config: dict):
        self.db_cfg = analytics_config['mysql']
        self.es_cfg = analytics_config['opensearch']

        self.pool = pooling.MySQLConnectionPool(
            **self.db_cfg
        )

        self.es = OpenSearch(
            hosts=[{'host': self.es_cfg['host'], 'port': self.es_cfg['port']}],
            http_auth=(self.es_cfg['user'], self.es_cfg['password']),
            use_ssl=True,
            verify_certs=False
        )
        print("SubscriberProfileLoader")

    def sync_es_to_db(self):
        print("[JOB] Running ES → DB sync job...")
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        index = self.es_cfg['index']
        table = "subscriberprofile"
        scroll = "2m"
        batch = self.es_cfg['batch_size']
        resp = self.es.search(index=index, scroll=scroll, size=batch, body={"query": {"match_all": {}}})
        scroll_id = resp["_scroll_id"]
        total = 0

        try:
            while True:
                hits = resp["hits"]["hits"]
                if not hits:
                    break
                for h in hits:
                    src = h["_source"]
                    sql = f"""
                        INSERT INTO {table} (
                            customerid, name, msisdn, activationdate,
                            channelid, currentsegment, churnscore,
                            created_at, updated_at
                        )
                        VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())
                        ON DUPLICATE KEY UPDATE
                            name=VALUES(name),
                            msisdn=VALUES(msisdn),
                            activationdate=VALUES(activationdate),
                            channelid=VALUES(channelid),
                            currentsegment=VALUES(currentsegment),
                            churnscore=VALUES(churnscore),
                            updated_at=NOW()
                    """
                    vals = (
                        src.get("customerid"), src.get("name"), src.get("msisdn"),
                        src.get("activationdate"), src.get("channelid"),
                        src.get("currentsegment"), src.get("churnscore")
                    )
                    cursor.execute(sql, vals)
                    total += 1
                conn.commit()
                resp = self.es.scroll(scroll_id=scroll_id, scroll=scroll)
                scroll_id = resp["_scroll_id"]
            print(f"[OK] Synced {total} records from ES to DB.")
        finally:
            if scroll_id:
                self.es.clear_scroll(scroll_id=scroll_id)
            cursor.close()
            conn.close()

    def update_churned(self):
        print("[JOB] Updating churned subscribers...")
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE subscriberprofile
            SET churndate = updated_at
            WHERE churndate IS NULL AND updated_at < CURDATE();
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("[OK] churned subscribers updated.")
