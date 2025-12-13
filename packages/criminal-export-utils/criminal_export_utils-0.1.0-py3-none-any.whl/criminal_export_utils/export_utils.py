import os
import pandas as pd
from datetime import datetime
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import QCoreApplication

def export_data_to_file(data, parent_widget=None, default_filename=None):
    if not data:
        QMessageBox.warning(parent_widget, "Експорт", "Немає даних для експорту.")
        return False
    
    if default_filename is None:
        default_filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    file_filter = "CSV файли (*.csv);;Excel файли (*.xlsx)"
    file_path, selected_filter = QFileDialog.getSaveFileName(
        parent_widget, 
        "Експорт даних", 
        os.path.expanduser(f"~/{default_filename}"), 
        file_filter
    )
    
    if not file_path:
        return False
    
    try:
        df = pd.DataFrame(data)
        
        if file_path.lower().endswith('.xlsx'):
            df.to_excel(file_path, index=False, engine='openpyxl')
        else:
            if not file_path.lower().endswith('.csv'):
                file_path += '.csv'
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
        
        QMessageBox.information(parent_widget, "Експорт", f"Дані успішно експортовано у файл:\n{file_path}")
        return True
    except Exception as e:
        QMessageBox.critical(parent_widget, "Помилка експорту", f"Помилка при експорті даних: {str(e)}")
        return False