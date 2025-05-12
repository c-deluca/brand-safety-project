query = """
SELECT url -- id, article_id, tipo, testata, title, url, testo, creation_timestamp, category 
FROM gd-gcp-prd-dp-lake-2-0.gd_gcp_prd_dp_lake_2_bq_0.cms_cms_atex_tutti_contenutieditoriali_snp 
where tipo = "video"
and testata = "repubblica"
and category in ("esteri")
and creation_timestamp between ("2025-04-01 00:00:00 UTC") and "2025-04-05 00:00:00 UTC"
order by creation_timestamp desc
limit 3
"""