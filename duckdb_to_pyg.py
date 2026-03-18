import os
import tempfile

import duckdb
from pygwalker.data_parsers.database_parser import Connector


def _visualize_record(self, record):
    self.viz_counter += 1
    label = f"可視化: {record.duckdb_name} [{self.viz_counter}]"
    try:
        # make_residence_list の処理は DataFrame 経由が必要なため内部のみで使用する
        processed_df = con.table(record.table_name).df()
        processed_df = self.mesh_pop.make_residence_list(processed_df)
        processed_df = processed_df.reset_index()

        # 処理済みデータを DuckDB 一時ファイルに書き込む
        # viz_original: 元データ（CSV マージのベースとして保持）
        # viz_display : PyGWalker が参照するテーブル
        temp_db_path = os.path.join(
            tempfile.gettempdir(),
            f"viz_{id(self)}_{self.viz_counter}.duckdb",
        )
        with duckdb.connect(temp_db_path) as tmp:
            tmp.execute("CREATE OR REPLACE TABLE viz_original AS SELECT * FROM processed_df")
            tmp.execute("CREATE OR REPLACE TABLE viz_display  AS SELECT * FROM processed_df")

        def make_connector() -> Connector:
            """DuckDB ファイルを SQLAlchemy Connector 経由で参照する（DataFrame を渡さない）"""
            return Connector(
                url=f"duckdb:///{temp_db_path}",
                view_sql="SELECT * FROM viz_display",
            )

        pyg_pane = pn.pane.HTML(
            pyg.to_html(make_connector()),
            sizing_mode='stretch_both',
            min_height=800,
        )
        file_input = pn.widgets.FileInput(accept='.csv')

        def load_and_merge_csv(event):
            if file_input.value is not None:
                self.mesh_pop.spinner.show()
                try:
                    added_df = pd.read_csv(io.BytesIO(file_input.value))
                    if 'dt' not in added_df.columns:
                        pn.state.notifications.error(
                            " 【エラー】読み込んだCSVファイルに時間データが存在しません。"
                        )
                        return

                    added_df['dt'] = pd.to_datetime(added_df['dt'])

                    # 元データ（viz_original）に CSV を結合して viz_display を更新
                    with duckdb.connect(temp_db_path) as tmp:
                        base_df = tmp.execute("SELECT * FROM viz_original").df()
                        combined_df = pd.concat([base_df, added_df], ignore_index=True)
                        tmp.execute(
                            "CREATE OR REPLACE TABLE viz_display AS SELECT * FROM combined_df"
                        )

                    pyg_pane.object = pyg.to_html(make_connector())
                    pn.state.notifications.success("CSVデータを読み込み、表示を更新しました。")
                except Exception as e:
                    logger.debug(f"エラー: {e}")
                    pn.state.notifications.error(
                        " 【エラー】読み込んだCSVファイルに時間データが存在しません。"
                    )
                finally:
                    self.mesh_pop.spinner.hide()

        file_input.param.watch(load_and_merge_csv, 'value')
        controls = pn.Row(pn.pane.Markdown("**比較用CSVを追加(dt, value...):**"), file_input, align="center")
        content = pn.Column(
            f"# {record.duckdb_name}_分析",
            controls,
            pyg_pane,
            sizing_mode='stretch_both'
        )
        self.tabs.append((label, content))
        record.tab_refs.append(label)
        self.tabs.active = len(self.tabs) - 1
