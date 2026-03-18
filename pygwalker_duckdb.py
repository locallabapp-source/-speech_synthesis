#!/usr/bin/env python3
"""
PyGWalker × DuckDB ダッシュボード
-------------------------------
依存ライブラリ:
  pip install streamlit pygwalker duckdb duckdb-engine sqlalchemy

起動:
  streamlit run pygwalker_duckdb.py
"""
import os
import tempfile

import duckdb
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
from pygwalker.data_parsers.database_parser import Connector

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Dashboard — PyGWalker × DuckDB")
st.caption("DuckDB ファイルDB → SQLAlchemy Connector → PyGWalker（DataFrame 変換なし）")

# DuckDB ファイルパス（tempdir に固定名で作成）
DB_PATH = os.path.join(tempfile.gettempdir(), "pygwalker_demo.duckdb")


# ----------------------------------------------------------------
# DuckDB ファイルにダミーデータを作成
# ----------------------------------------------------------------

def setup_database(db_path: str) -> None:
    """初回のみダミーデータを作成する"""
    conn = duckdb.connect(db_path)
    conn.execute("""
        CREATE OR REPLACE TABLE sales AS
        SELECT
            i + 1                                            AS id,
            DATE '2024-01-01' + CAST(i * 13 % 365 AS INTEGER) AS sale_date,
            CASE i % 5
                WHEN 0 THEN 'Electronics'
                WHEN 1 THEN 'Clothing'
                WHEN 2 THEN 'Food & Beverage'
                WHEN 3 THEN 'Books'
                ELSE        'Furniture'
            END                                              AS category,
            CASE i % 5
                WHEN 0 THEN 'Tokyo'
                WHEN 1 THEN 'Osaka'
                WHEN 2 THEN 'Nagoya'
                WHEN 3 THEN 'Fukuoka'
                ELSE        'Sapporo'
            END                                              AS region,
            CASE i % 3
                WHEN 0 THEN '田中'
                WHEN 1 THEN '鈴木'
                ELSE        '佐藤'
            END                                              AS sales_rep,
            CASE i % 4
                WHEN 0 THEN 'Online'
                WHEN 1 THEN 'Store'
                WHEN 2 THEN 'Phone'
                ELSE        'Partner'
            END                                              AS channel,
            ROUND((i * 37 % 950) + 50.0, 2)                 AS amount,
            (i * 7  % 9) + 1                                 AS quantity,
            ROUND(
                ((i * 37 % 950) + 50.0) * ((i * 7 % 9) + 1),
                2
            )                                                AS total_amount
        FROM range(500) t(i)
    """)
    conn.close()


# ----------------------------------------------------------------
# PyGWalker Connector（SQLAlchemy 経由で DuckDB を参照）
# ----------------------------------------------------------------

@st.cache_resource
def get_renderer() -> StreamlitRenderer:
    setup_database(DB_PATH)
    # duckdb+duckdb:/// でファイルDBに接続 — DataFrame は生成しない
    connector = Connector(
        url=f"duckdb:///{DB_PATH}",
        view_sql="SELECT * FROM sales",
    )
    return StreamlitRenderer(connector, spec="", debug=False)


# ----------------------------------------------------------------
# ページ描画
# ----------------------------------------------------------------

with st.expander("データプレビュー（先頭 10 件）", expanded=False):
    conn = duckdb.connect(DB_PATH) if os.path.exists(DB_PATH) else None
    if conn:
        st.dataframe(conn.sql("SELECT * FROM sales LIMIT 10").df())
        conn.close()

renderer = get_renderer()
renderer.explorer()
