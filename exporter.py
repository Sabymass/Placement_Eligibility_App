# exporter.py
from io import BytesIO
import pandas as pd

class ExcelExporter:
    @staticmethod
    def export_to_excel(export_data):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for sheet, df in export_data.items():
                df.to_excel(writer, index=False, sheet_name=sheet)
        output.seek(0)
        return output
