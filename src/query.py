query = """SELECT url -- id, article_id, tipo, testata, title, url, testo, creation_timestamp, category 
FROM gd-gcp-prd-dp-lake-2-0.gd_gcp_prd_dp_lake_2_bq_0.cms_cms_atex_tutti_contenutieditoriali_snp 
where tipo = "video"
and testata = "repubblica"
and category in ("esteri", "cronaca")
and creation_timestamp between ("2024-12-01 00:00:00 UTC") and "2025-01-01 00:00:00 UTC"
--and url like any ('%contraff%')
--and url like any ('%cuba_sfila%') --'%gdf_novara%', '%a_cuba_sfila%', '%nave_italiana%', '%gli_avvocati_di_via_poma%') --'%parisi_del_sismi%', '%spari_nella_notte_a_perugia%')
--and url like any ('%mar_nero_caccia%') --'%guerra%', '%ebrei%', '%pace%', '%sostanz%', '%sess%', '%alcol%')
--order by creation_timestamp 
limit 15
"""
