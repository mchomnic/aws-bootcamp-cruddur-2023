from datetime import datetime, timedelta, timezone
import logging

from lib.db import pool, query_wrap_array

class HomeActivities:
  def run(logger : logging, cognito_user_id: str=None):
    # now = datetime.now(timezone.utc).astimezone()
    logger.info("HomeActivities")

    sql = query_wrap_array("""
      SELECT
        activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities
      LEFT JOIN public.users ON users.uuid = activities.user_uuid
      ORDER BY activities.created_at DESC
    """)
    # logger.info("===============")
    # logger.info(sql)
    # logger.info("===============")
    with pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql)
        # this will return a tuple
        # the first field being the data
        json = cur.fetchone()
    logger.info(json)
    return json[0]

    return results