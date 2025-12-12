import xlsxwriter
import datetime
from collections import defaultdict
import pytz
from analytics_sdk.utilities import (
    APP_ID,
    APP_DISPLAY_NAME,
    upload_file
)
    
def lastColumnOfChart(chart_width,chart_pos):
    return int(-(-chart_width*9//553))+ord(chart_pos[0])-1


class ExcelWriter:

    DATA_PER_SHEET_LIMIT = 1000001
    ROW_START = 3
    CONTENT_ROW_START = 0
    def __init__(self, run_id, file_name, app_id):
        self.run_id = run_id
        self.file_name = file_name
        self.app_id = app_id
        self.wb = xlsxwriter.Workbook(self.file_name, {'constant_memory':True, 'nan_inf_to_errors': True})
        self.total_sheet_row_counts = {}
        self.active_sheet_title = ''
        self.sheet_refs = {}
        self.run_params = None


    def create_sheet(self, sheet_title):
        sheet_title = self.get_page_title(sheet_title, 0)
        if sheet_title in self.sheet_refs:
            return self.sheet_refs[sheet_title]
        ws = self.wb.add_worksheet(sheet_title)
        self.sheet_refs[sheet_title] = ws
        # self.add_headers(ws)
        return ws
    
    def close_wb(self):
        if self.wb:
            self.wb.close()
    
    def get_page_title(self, title, page_no):
        pg_title = ''
        if page_no > 0:
            pg_title = f'.. {page_no}'
        pg_title_len = len(pg_title)
        remain_len = 29 - pg_title_len
        title = title[0:remain_len]
        title = title + pg_title
        return title
    

    def write_summary_data(self, summary_data):
        ws = self.create_sheet('SUMMARY')
        self.fill_sheet_bg_colors(ws)
        ws.set_column('B:B', 24)
        ws.set_column('C:C', 24)
        # Rendering Run Summary information
        if summary_data is not None and len(summary_data) > 0:
            cell_no = ExcelWriter.ROW_START
            for entry in summary_data:
                ws.write(f'B{cell_no}', entry, self.wb.add_format({'color':'00598B', 'bg_color' : 'eeeeee'}))
                ws.write(f'C{cell_no}', summary_data[entry], self.wb.add_format({'color':'000000', 'bg_color' : 'eeeeee'}))
                cell_no += 1
            if self.run_params and self.run_params is not None and len(self.run_params) > 0:
                opsql_params = None
                if 'opsql_query' in self.run_params:
                    opsql_params = self.run_params['opsql_query']
                if opsql_params is not None:
                    for key in opsql_params.keys():
                        display_name = self.get_display_name(key)
                        display_value = self.get_display_value(opsql_params[key])

                        ws.write(f'B{cell_no}', display_name, self.wb.add_format({'color':'00598B', 'bg_color' : 'eeeeee'}))
                        ws.write(f'C{cell_no}', display_value, self.wb.add_format({'color':'000000', 'bg_color' : 'eeeeee'}))
                        cell_no += 1
        


    def write_glossary_data(self, glossary_data):
        ws = self.create_sheet('GLOSSARY')
        if ws:
            self.fill_sheet_bg_colors(ws)
            data_len = 30
            if glossary_data is not None and len(glossary_data) >= data_len:
                data_len = len(glossary_data)+5
            
            # self.fill_sheet_bg_colors(ws, start_row=1, end_row=data_len)
            ws.set_column('B:B', 50)
            ws.set_column('C:C', 24)

            cell_no = 3
            if glossary_data is not None:
                data = glossary_data
                for key in data.keys():
                    display_name = key
                    display_value = data[key]

                    ws.write(f'B{cell_no}', display_name, self.wb.add_format({'color':'00598B', 'bg_color' : 'eeeeee'}))
                    ws.write(f'C{cell_no}', display_value, self.wb.add_format({'color':'000000', 'bg_color' : 'eeeeee'}))

                    cell_no += 1


    def get_value(self, value):
        if value:
            try:
                value = float(value)
                return value
            except ValueError:
                return value
            except Exception as e:
                return value
        return value
    

    def _prepare_chunk_data(self, data, _chunk_size):
        chunk_data = []
        for _record in data:
            chunk_data.append(_record)
            if len(chunk_data) >= _chunk_size:
                yield chunk_data
                chunk_data = []
        if chunk_data:
            yield chunk_data
    
    
    def render_table(self, ws, title, headers, data, row_start=1, col_start=1):
        if APP_ID == 'AVAILABILITY-DETAILS':
            self.render_available_details_table(ws, title, headers, data, row_start, col_start)
            return
        
        column_widths = {}
        row_no = ExcelWriter.CONTENT_ROW_START - 1 + row_start
        # Adding table title here
        header_format = self.wb.add_format({'bold': True, 'border': 1, 'bg_color': '#7D92AF', 'font_color':'#FFFFFF', 'border': 2, 'border_color': '#FFFFFF'})
        data_format = self.wb.add_format({'bg_color': '#DCE6F1', 'border': 1, 'border_color': '#FFFFFF'})
        if headers:
            ws.write_row(row_no, 0, headers[0], header_format)
            for col_delta, val in enumerate(headers[0]):
                column_widths[col_delta] = max(len(str(val)), 8)
            row_no += 1

        _chunk_size = 10000
        _row_count = 0
        for chunk_data in self._prepare_chunk_data(data, _chunk_size):
            for row_delta, _row in enumerate(chunk_data):
                _row_count +=1
                
                ws.write_row(row_no, 0, _row, data_format)
                for col_delta, val in enumerate(_row):
                    if col_delta in column_widths:
                        column_widths[col_delta] = max(len(str(val)), column_widths[col_delta])
                    else:
                        column_widths[col_delta] = max(len(str(val)), 8)
                row_no += 1
            del chunk_data
            
        for col, column_width in column_widths.items():
            col_name = xlsxwriter.utility.xl_col_to_name(col)
            ws.set_column(f'{col_name}:{col_name}', column_width + 2)


    def render_metric_table(self, ws, component_data, merge_cells, title, headers, data, row_start=1, col_start=1):
        column_widths = {}
        if data:
            if merge_cells:
                for merge_cell in merge_cells:
                    ws.merge_range(merge_cell, '')
            
            row_no = ExcelWriter.CONTENT_ROW_START - 1 + row_start
            
            header_format = self.wb.add_format({'align': 'center', 'bold': True, 'bg_color': '#7D92AF', 'font_color':'#FFFFFF', 'border': 0, 'border_color': '#FFFFFF'})
            data_format = self.wb.add_format({'bg_color': '#DCE6F1', 'border': 1, 'border_color': '#FFFFFF'})
            if headers:
                for header in headers:
                    ws.write_row(row_no, 0, header, header_format)
                    for col_delta, val in enumerate(header):
                        if col_delta in column_widths:
                            column_widths[col_delta] = max(len(str(val)), column_widths[col_delta])
                        else:
                            column_widths[col_delta] = max(len(str(val)), 8)
                    row_no += 1

            _chunk_size = 10000
            for chunk_data in self._prepare_chunk_data(data, _chunk_size):
                for row_delta, _row in enumerate(chunk_data):
                    ws.write_row(row_no, 0, _row, data_format)
                    for col_delta, val in enumerate(_row):
                        if col_delta in column_widths:
                            column_widths[col_delta] = max(len(str(val)), column_widths[col_delta])
                        else:
                            column_widths[col_delta] = max(len(str(val)), 8)
                    row_no += 1
                del chunk_data
            
            for col, column_width in column_widths.items():
                col_name = xlsxwriter.utility.xl_col_to_name(col)
                ws.set_column(f'{col_name}:{col_name}', column_width + 2)

                

    def render_available_details_table(self, ws, title, headers, data, row_start=1, col_start=1):
        column_widths = {}
        row_no = ExcelWriter.CONTENT_ROW_START - 1 + row_start
        header_format = self.wb.add_format({'bold': True, 'border': 1, 'bg_color': '#7D92AF', 'font_color':'#FFFFFF', 'border': 2, 'border_color': '#FFFFFF'})
        # Adding table title here
        if headers:
            ws.write_row(row_no, 0, headers[0], header_format)

            for col_delta, val in enumerate(headers[0]):
                column_widths[col_delta] = max(len(str(val)), 8)
            row_no += 1

        _chunk_size = 10000
        for chunk_data in self._prepare_chunk_data(data, _chunk_size):
            for row_delta, _row in enumerate(chunk_data):
                for col_delta, val in enumerate(_row):
                    cell_position = xlsxwriter.utility.xl_rowcol_to_cell(row_no, col_delta-1+col_start)
                    bg_color = '#DCE6F1'
                    try:
                        if APP_ID == 'AVAILABILITY-DETAILS':
                            if isinstance(val, str) and 'COLOR-CODE_' in val:
                                vals = val.split('_') #COLOR-CODE_{color_code}_100.0
                                if len(vals) == 3:
                                    val = vals[2]
                                    if vals[1] is not None and len(vals[1]):
                                        bg_color = vals[1]
                        val = self.get_value(val)
                    except Exception as e:
                            print('ExcelWriter: found exception... value is :: ', val)
                            try:
                                val = str(val)
                            except Exception as ex:
                                val = ''
                    ws.write(cell_position, val, self.wb.add_format({'bg_color': bg_color, 'border': 1, 'border_color': '#FFFFFF'}))
                    if col_delta in column_widths:
                        column_widths[col_delta] = max(len(str(val)), column_widths[col_delta])
                    else:
                        column_widths[col_delta] = max(len(str(val)), 8)
                row_no += 1
            del chunk_data

        for col, column_width in column_widths.items():
            col_name = xlsxwriter.utility.xl_col_to_name(col)
            ws.set_column(f'{col_name}:{col_name}', column_width + 2)



    def render_old_table(self, ws, title, headers, data, row_start=1, col_start=1):
        column_widths = {}
        if data:
            sheet_count = 1
            # ws = self.create_sheet(title)
            #self.add_headers(ws)
            new_title = title
            self.active_sheet_title = title
            if self.active_sheet_title not in self.total_sheet_row_counts:
                self.total_sheet_row_counts[self.active_sheet_title] = 0
            row_no = ExcelWriter.CONTENT_ROW_START - 1 + row_start
            if new_title in self.total_sheet_row_counts and self.total_sheet_row_counts[new_title] > 0:
                row_no = self.total_sheet_row_counts[new_title]
            for row_delta, _row in enumerate(data):
                if self.total_sheet_row_counts[new_title] >= ExcelWriter.DATA_PER_SHEET_LIMIT:
                    row_no = ExcelWriter.CONTENT_ROW_START - 1 + row_start
                    new_title = self.get_page_title(title, sheet_count)
                    sheet_count += 1
                    self.active_sheet_title = new_title
                    # ws = self.create_sheet(new_title)
                    self.add_headers(ws)
                    if self.active_sheet_title not in self.total_sheet_row_counts:
                        self.total_sheet_row_counts[self.active_sheet_title] = 0
                if row_no == ExcelWriter.CONTENT_ROW_START:
                    # Adding table title here
                    # ws.write_row(row_no-1, 0, [title], self.wb.add_format({'font_color': '00598B', 'bold':True}))
                    ws.write_row(row_no, 0, headers[0], self.wb.add_format({'bold': True, 'border': 1, 'bg_color': '#7D92AF', 'font_color':'#FFFFFF', 'border': 2, 'border_color': '#FFFFFF'}))
                    row_no += 1
                for col_delta, val in enumerate(_row):
                    cell_position = xlsxwriter.utility.xl_rowcol_to_cell(row_no, col_delta)
                    bg_color = '#DCE6F1'
                    try:
                        if APP_ID == 'AVAILABILITY-DETAILS':
                            if isinstance(val, str) and 'COLOR-CODE_' in val:
                                vals = val.split('_') #COLOR-CODE_{color_code}_100.0
                                if len(vals) == 3:
                                    val = vals[2]
                                    if vals[1] is not None and len(vals[1]):
                                        bg_color = vals[1]
                        val = self.get_value(val)
                    except Exception as e:
                        print('ExcelWriter: found exception... value is :: ', val)
                        try:
                            val = str(val)
                        except Exception as ex:
                            val = ''
                    ws.write(cell_position, val, self.wb.add_format({'bg_color': bg_color, 'border': 1, 'border_color': '#FFFFFF'}))
                    if col_delta in column_widths:
                        column_widths[col_delta] = max(len(str(val)), column_widths[col_delta])
                    else:
                        column_widths[col_delta] = max(len(str(val)), 8)
                row_no += 1
                self.total_sheet_row_counts[new_title] = row_no
        for col, column_width in column_widths.items():
            col_name = xlsxwriter.utility.xl_col_to_name(col)
            ws.set_column(f'{col_name}:{col_name}', column_width + 2)

    
    def prepare_report_summary_data(self, run_id, run_summary, tenant_info, user_params, run_start_time, run_completion_time):
        summary_data = {}
        summary_data['App'] = APP_DISPLAY_NAME.replace('-', ' ').title()
        c_name = ''
        if tenant_info is not None and len(tenant_info) > 0:
            result = self.client_names_ids(tenant_info)
            c_name = result[0]
        summary_data['Tenant Name'] = c_name
        summary_data['Run date'] = run_start_time
        summary_data['Completion date'] = run_completion_time
        first_name = run_summary.json()['analysisRun']['createdBy']['firstName']
        last_name = run_summary.json()['analysisRun']['createdBy']['lastName']
        login_name = run_summary.json()['analysisRun']['createdBy']['loginName']
        summary_data['User'] = f'{first_name} {last_name} ({login_name})'
        if user_params is not None:
            for key in user_params.keys():
                summary_data[self.get_display_name(key)] = self.get_display_value(user_params[key])
        return summary_data
    
                                                                                                                                                                                     
    def add_headers(self, ws):
        ws.merge_range('A1:A2', '')
        ws.merge_range('B1:Z2', '')
        ws.write('B1', self.app_id.title(), self.wb.add_format({'font_color': '00598B', 'bg_color': 'eeeeee', 'bold':True, 'align':'vcenter'}))
        ws.write('A1', '', self.wb.add_format({'font_color': '00598B', 'bg_color': 'eeeeee'}))


    def _set_title_as_header(self, ws, sheet_data):
        header_format = self.wb.add_format({'bold': True, 'font_color': '#00598B', 'align': 'left', 'valign': 'vcleft', 'font_size': 12, # 'bg_color': '#eeeeee'
            })

        row_format = self.wb.add_format({'bg_color': '#eeeeee'     # Row background fill color
        })

        # Apply row formatting to rows above header
        for row_idx in range(1):  # 0-based indexing; 'ROW_START - 1'
            ws.set_row(row_idx, None, row_format)  # Set row format
        ws.merge_range('A1:RR2', sheet_data['insights-title-header'].replace('-', ' ').title(), header_format)


    def fill_sheet_bg_colors(self, ws, start_row=0, end_row=30, fill_type="solid", color="eeeeee"):
        if ws:
            format=self.wb.add_format({'bg_color': color})
            ws.conditional_format(start_row, 0, end_row, 30, {'type': 'blanks', 'format': format})
            # ws.conditional_format(f'A{start_row}:C{end_row}', {'type': 'no_blanks', 'format': format})
            # ws.set_column(0, 30, None, self.wb.add_format({'bg_color': color}))
            # ws.set_row(0, 30, self.wb.add_format({'bg_color': 'eeeeee'}))

    def generate_excel_file(self, form, resp, report_summary_data, reportname, filepath):
        if resp:
            if 'excel-data' in resp:
                excel_data = []
                excel_data.append(
                    {
                        'title': 'SUMMARY',
                        'summary' : 'true',
                        'header': {},
                        'data': report_summary_data
                    }
                )
                if 'sheets' in resp['excel-data']:
                    for sheet in resp['excel-data']['sheets']:
                        excel_data.append(sheet)
                resp['excel-data']['sheets'] = excel_data
                self.render(resp['excel-data'])
                self.wb.close()
                # saving excel file
                excel_url = upload_file(form.get_run_id(), reportname, filepath)
                resp['excel_url'] = excel_url
        return resp

    
    def client_names_ids(self, customer_name):
        names = ''
        client_id = ''
        if customer_name and customer_name is not None:
            for i in customer_name:
                for j in i.items():
                    names+=j[1]['name']
                    client_id+=j[1]['uniqueId']
                    names+=', '
                    client_id+=', '
            names = names.rstrip(', ')
            client_id = client_id.rstrip(', ')
            return names, client_id
        else:
            return names, client_id
        

    def get_display_name(self, key):
        if key == 'filterCriteria':
            return 'Query'
        if key == 'fields':
            return 'Attributes'
        if key == 'groupBy':
            return 'Group By'
        if key == 'soryBy':
            return 'Sort By'
        if key == 'sortByOrder':
            return 'Sort By Order'
        return key


    def get_display_value(self, value):
        if value is None and len(value) <= 0:
            return '-'
        else:
            if isinstance(value, list):
                all_values = ', '.join([val for val in value])
                return all_values
        return value
    
        
    def add_doughnut_chart(self,ws,component_data):
        chart=self.wb.add_chart({'type':'doughnut', 'name':component_data['chart-title']})
        cell_format1 = self.wb.add_format()
        cell_format1.set_bold()
        cell_format1.set_font_color('#0066CC')

        # inserting data to our sheet
        cell_position = xlsxwriter.utility.xl_rowcol_to_cell(component_data['start-row']-2, component_data['start-col']-1)
        ws.write(cell_position, component_data['chart-title'], cell_format1)
        row_number=component_data['start-row']-1
        for row_delta, row_val in enumerate(component_data['data']):
            for col_delta, val in enumerate(row_val):
                cell_position = xlsxwriter.utility.xl_rowcol_to_cell((row_number + row_delta), component_data['start-col'] - 1 + col_delta)
                if row_delta == 0:
                    ws.write(cell_position, self.get_value(val), self.wb.add_format({'bold': True, 'border': 1, 'bg_color': '#7D92AF', 'font_color':'#FFFFFF', 'border': 2, 'border_color': '#FFFFFF'}))
                else:
                    ws.write(cell_position, self.get_value(val))
                    # ws.write(cell_position, val, self.wb.add_format({'bg_color': '#DCE6F1', 'border': 1, 'border_color': '#FFFFFF'}))

        colors=["#0077C8", "#00A3E0", "#673AB7", "#9C27B0", "#E91E63", "#F47925"]
        color_fill = []
        for i in colors:
            color_fill.append({"fill": {"color": i}})

        series_data = {
                "categories":f"='{ws.name}'!${chr(component_data['start-col']+64)}${component_data['start-row']+1}:${chr(component_data['start-col']+64)}${len(component_data['data'])+component_data['start-row']-1}",
                "values":f"='{ws.name}'!${chr(component_data['start-col']+65)}${component_data['start-row']+1}:${chr(component_data['start-col']+65)}${len(component_data['data'])+component_data['start-row']-1}",
                "points" : color_fill
            }
        chart.add_series(
            series_data
        )

        if 'width' in component_data:     
            chart.set_size({'width':component_data['width']*0.36*96,'height':component_data['height']*0.388*96})
            if lastColumnOfChart(component_data['width']*0.36*96,component_data['chart-position'])>=component_data['start-col'] and ord(component_data['chart-position'][0])<component_data['start-col']+64:
                ws.set_column_pixels(component_data['start-col']-2,component_data['start-col']-2,558)
        
        chart.set_title({'name':component_data['chart-title'],'name_font':{'color':'black'}})

        chart.set_style(10)

        if "hole-size" in component_data:
            chart.set_hole_size(component_data["hole-size"])

        ws.insert_chart(component_data['chart-position'], chart)     
        
    
    
    def add_pie_chart(self,ws,component_data):
        chart=self.wb.add_chart({'type':'pie'})
        cell_format=self.wb.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('#0066CC')
        # inserting data row-wise as we have the data in our map row-wise only
        ws.write(component_data['start-row']-2,component_data['start-col']-1,component_data['chart-title'],cell_format)
        row_number=component_data['start-row']-1
        lst=component_data['data']
        ptr=0
        while  ptr<len(component_data['data']):
            ws.write_row(row_number,component_data['start-col']-1,lst[ptr])        
            row_number+=1
            ptr+=1 

        colors=["#0077C8", "#00A3E0", "#673AB7", "#9C27B0", "#E91E63", "#F47925"]
        color_fill = []
        for i in colors:
           color_fill.append({"fill": {"color": i}})  
        chart.add_series(
            {
                "categories":f"='{ws.name}'!${chr(component_data['start-col']+64)}${component_data['start-row']+1}:${chr(component_data['start-col']+64)}${len(component_data['data'])+component_data['start-row']-1}",
                "values":f"='{ws.name}'!${chr(component_data['start-col']+65)}${component_data['start-row']+1}:${chr(component_data['start-col']+65)}${len(component_data['data'])+component_data['start-row']-1}",
                # filling the custom colors to chart
                "points" : color_fill,
            }
        )
        if 'width' in component_data:
            chart.set_size({'width':component_data['width']*0.36*96,'height':component_data['height']*0.388*96})
            if lastColumnOfChart(component_data['width']*0.36*96,component_data['chart-position'])>=component_data['start-col'] and ord(component_data['chart-position'][0])<component_data['start-col']+64:
                ws.set_column_pixels(component_data['start-col']-2,component_data['start-col']-2,558)
        chart.set_title({'name':component_data['chart-title'],'name_font':{'color':'black'}})
        if 'hole-size' in component_data:
            chart.set_hole_size(component_data['hole-size'])
        ws.insert_chart(component_data['chart-position'],chart)  


    # def add_bar_chart(self,ws,component_data):
    #     chart=self.wb.add_chart({"type":"column"})
    #     cell_format=self.wb.add_format()
    #     cell_format.set_bold()
    #     cell_format.set_font_color('#00598B')
    #     # inserting data row-wise as we have the data in our map row-wise only
    #     ws.write(component_data['start-row']-2,component_data['start-col']-1,component_data['chart-title'],cell_format)
    #     row_number=component_data['start-row']-1
    #     lst=component_data['data']
    #     ptr=0
    #     while  ptr<len(component_data['data']):
    #         ws.write_row(row_number,component_data['start-col']-1,lst[ptr])
    #         row_number+=1
    #         ptr+=1

    #     ptr2=component_data['start-col']+1
    #     while(ptr2<len(component_data['data'][0])+component_data['start-col']):
    #         chart.add_series(
    #             {
    #                 "name":f"='{ws.name}'!${chr(ptr2+64)}${component_data['start-row']}",
    #                 "categories":f"='{ws.name}'!${chr(component_data['start-col']+64)}${component_data['start-row']+1}:${chr(component_data['start-col']+64)}${len(component_data['data'])+component_data['start-row']-1}",
    #                 "values":f"='{ws.name}'!${chr(ptr2+64)}${component_data['start-row']+1}:${chr(ptr2+64)}${len(component_data['data'])+component_data['start-row']-1}",
    #             }
    #         )
    #         ptr2+=1

    #     # Set custom bar colors if provided
    #     # Check if the chart should be multicolored
    #     if component_data.get('is-multicolored-chart', False):
    #         colors = component_data.get('colors', [])
    #         for i, color in enumerate(colors):
    #             chart.add_series({
    #             "categories": f"='{ws.name}'!${chr(component_data['start-col'] + 64)}${component_data['start-row'] + i + 1}",
    #             "values": f"='{ws.name}'!${chr(component_data['start-col'] + 65)}${component_data['start-row'] + i + 1}",
    #             "fill": {"color": color},
    #         })

    #     if 'width' in component_data:
    #         chart.set_size({'width':component_data['width']*0.36*96,'height':component_data['height']*0.388*96})
    #         if lastColumnOfChart(component_data['width']*0.36*96,component_data['chart-position'])>=component_data['start-col'] and ord(component_data['chart-position'][0])<component_data['start-col']+64:
    #             ws.set_column_pixels(component_data['start-col']-2,component_data['start-col']-2,558)
    #     chart.set_title({"name":component_data['chart-title'],'name_font':{'color':'black'}})
    #     chart.set_x_axis({"name":component_data['x-axis-title']})
    #     chart.set_y_axis({"name":component_data['y-axis-title']})
    #     ws.insert_chart(component_data['chart-position'],chart)



    def add_bar_chart(self, ws, component_data):
        for row_num, row_data in enumerate(component_data['data']):
            ws.write_row(row_num + component_data['start-row'], component_data['start-col'], row_data)

        chart = self.wb.add_chart({'type': 'column'})

        last_row = component_data['start-row'] + len(component_data['data'])

        bar_gap = None
        if 'bar-gap' in component_data and component_data['bar-gap'] is not None:
            bar_gap = component_data['bar-gap']
        chart.add_series({
            'categories': f"='{ws.name}'!${chr(65 + component_data['start-col'])}{component_data['start-row'] + 2}:"
                          f"${chr(65 + component_data['start-col'])}{last_row}",
            'values': f"='{ws.name}'!${chr(66 + component_data['start-col'])}{component_data['start-row'] + 2}:"
                      f"${chr(66 + component_data['start-col'])}{last_row}",
            'name': component_data['data'][0][1],
            'fill': {'color': component_data['colors'][0]},
            'gap': bar_gap
        })

        chart.set_title({'name': component_data['chart-title'], 'name_font': {'color': component_data['title-color']}})
        chart.set_legend({'position': 'none'})

        chart.set_x_axis({
            'name': component_data['x-axis-title'],
            'min': 0,  # Minimum range for X-axis
            'max': len(component_data['data']) - 2,  # Maximum range for X-axis (based on number of categories)
        })

        chart.set_y_axis({'name': component_data['y-axis-title'], 'min': 0})

        chart.set_size({'width': component_data['width'], 'height': component_data['height']})
        ws.insert_chart(component_data['chart-position'], chart)

    
    def add_scatter_chart(self,ws,component_data):
        chart=self.wb.add_chart({"type":"scatter"}) 
        cell_format=self.wb.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('#0066CC')
        # inserting data row-wise as we have the data in our map row-wise only
        ws.write(component_data['start-row']-2,component_data['start-col']-1,component_data['chart-title'],cell_format)
        row_number=component_data['start-row']-1
        lst=component_data['data']
        ptr=0
        while  ptr<len(component_data['data']):
            ws.write_row(row_number,component_data['start-col']-1,lst[ptr])        
            row_number+=1
            ptr+=1
        ptr2=component_data['start-col']+1
        while(ptr2<len(component_data['data'][0])+component_data['start-col']):
            chart.add_series(
                {
                    "name":f"='{ws.name}'!${chr(ptr2+64)}${component_data['start-row']}",
                    "categories":f"='{ws.name}'!${chr(component_data['start-col']+64)}${component_data['start-row']+1}:${chr(component_data['start-col']+64)}${len(component_data['data'])+component_data['start-row']-1}",
                    "values":f"='{ws.name}'!${chr(ptr2+64)}${component_data['start-row']+1}:${chr(ptr2+64)}${len(component_data['data'])+component_data['start-row']-1}",
                }
            )
            ptr2+=1
        if 'width' in component_data:
            chart.set_size({'width':component_data['width']*0.36*96,'height':component_data['height']*0.388*96})
            if lastColumnOfChart(component_data['width']*0.36*96,component_data['chart-position'])>=component_data['start-col'] and ord(component_data['chart-position'][0])<component_data['start-col']+64:
                ws.set_column_pixels(component_data['start-col']-2,component_data['start-col']-2,558)
        chart.set_title({"name":component_data['chart-title'],'name_font':{'color':'black'}})
        chart.set_x_axis({"name":component_data['x-axis-title']})
        chart.set_y_axis({"name":component_data['y-axis-title']})
        ws.insert_chart(component_data['chart-position'],chart)       

    def add_line_chart(self,ws,component_data):
        chart=self.wb.add_chart({"type":"line"}) 
        cell_format=self.wb.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('#0066CC')
        # inserting data row-wise as we have the data in our map row-wise only
        ws.write(component_data['start-row']-2,component_data['start-col']-1,component_data['chart-title'],cell_format)
        row_number=component_data['start-row']-1
        lst=component_data['data']
        ptr=0
        while  ptr<len(component_data['data']):
            ws.write_row(row_number,component_data['start-col']-1,lst[ptr])        
            row_number+=1
            ptr+=1 
        ptr2=component_data['start-col']+1
        while(ptr2<len(component_data['data'][0])+component_data['start-col']):
            chart.add_series(
                {
                    "name":f"='{ws.name}'!${chr(ptr2+64)}${component_data['start-row']}",
                    "categories":f"='{ws.name}'!${chr(component_data['start-col']+64)}${component_data['start-row']+1}:${chr(component_data['start-col']+64)}${len(component_data['data'])+component_data['start-row']-1}",
                    "values":f"='{ws.name}'!${chr(ptr2+64)}${component_data['start-row']+1}:${chr(ptr2+64)}${len(component_data['data'])+component_data['start-row']-1}",
                }
            )
            ptr2+=1
        if 'width' in component_data:
            chart.set_size({'width':component_data['width']*0.36*96,'height':component_data['height']*0.388*96})
            if lastColumnOfChart(component_data['width']*0.36*96,component_data['chart-position'])>=component_data['start-col'] and ord(component_data['chart-position'][0])<component_data['start-col']+64:
                ws.set_column_pixels(component_data['start-col']-2,component_data['start-col']-2,558)
        chart.set_title({"name":component_data['chart-title'],'name_font':{'color':'black'}})
        chart.set_x_axis({"name":component_data['x-axis-title']})
        chart.set_y_axis({"name":component_data['y-axis-title']})
        ws.insert_chart(component_data['chart-position'],chart)


    def add_stack_bar_chart(self,ws,component_data):
        chart=self.wb.add_chart({"type":"line","subtype":"stacked"}) 
        cell_format=self.wb.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('#0066CC')
        # inserting data row-wise as we have the data in our map row-wise only
        ws.write(component_data['start-row']-2,component_data['start-col']-1,component_data['chart-title'],cell_format)
        row_number=component_data['start-row']-1
        lst=component_data['data']
        ptr=0
        while  ptr<len(component_data['data']):
            ws.write_row(row_number,component_data['start-col']-1,lst[ptr])        
            row_number+=1
            ptr+=1
        ptr2=component_data['start-col']+1
        while(ptr2<len(component_data['data'][0])+component_data['start-col']):
            chart.add_series(
                {
                    "name":f"='{ws.name}'!${chr(ptr2+64)}${component_data['start-row']}",
                    "categories":f"='{ws.name}'!${chr(component_data['start-col']+64)}${component_data['start-row']+1}:${chr(component_data['start-col']+64)}${len(component_data['data'])+component_data['start-row']-1}",
                    "values":f"='{ws.name}'!${chr(ptr2+64)}${component_data['start-row']+1}:${chr(ptr2+64)}${len(component_data['data'])+component_data['start-row']-1}",
                }
            )
            ptr2+=1
        if 'width' in component_data:
            chart.set_size({'width':component_data['width']*0.36*96,'height':component_data['height']*0.388*96})
            if lastColumnOfChart(component_data['width']*0.36*96,component_data['chart-position'])>=component_data['start-col'] and ord(component_data['chart-position'][0])<component_data['start-col']+64:
                ws.set_column_pixels(component_data['start-col']-2,component_data['start-col']-2,558)
        chart.set_title({"name":component_data['chart-title'],'name_font':{'color':component_data['title-color']}})
        chart.set_x_axis({"name":component_data['x-axis-title']})
        chart.set_y_axis({"name":component_data['y-axis-title']})
        ws.insert_chart(component_data['chart-position'],chart,{'x_scale':component_data['chart-width'],'y_scale':component_data['chart-height']})


    def add_bar_line_trend_chart(self,ws,component_data):
        cell_format=self.wb.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('#0066CC')
        # inserting data row-wise as we have the data in our map row-wise only
        ws.write(component_data['start-row']-2,component_data['start-col']-1,component_data['chart-title'],cell_format)
        row_number=component_data['start-row']-1
        lst=component_data['data']
        ptr=0
        while  ptr<len(component_data['data']):
            ws.write_row(row_number,component_data['start-col']-1,lst[ptr])      
            row_number+=1
            ptr+=1
        ws.set_column(f'{chr(component_data["start-col"]+64)}:{chr(component_data["start-col"]+64)}',80)
        chart1 = self.wb.add_chart({"type": "column"})
        # adding data series to the chart 
        # if 'x-axis-date-format' in component_data:
        ptr1=component_data['start-col']+1
        while(ptr1<len(component_data['data'][0])+component_data['start-col']):
            chart1.add_series(
                {
                    "name":f"='{ws.name}'!${chr(ptr1+64)}${component_data['start-row']}",
                    # "date_axis":True,
                    "categories":f"='{ws.name}'!${chr(component_data['start-col']+64)}${component_data['start-row']+1}:${chr(component_data['start-col']+64)}${len(component_data['data'])+component_data['start-row']-1}",
                    "values":f"='{ws.name}'!${chr(ptr1+64)}${component_data['start-row']+1}:${chr(ptr1+64)}${len(component_data['data'])+component_data['start-row']-1}",
                }
            )
            ptr1+=1   
        chart2 = self.wb.add_chart({"type": "line"})
        # adding data series to the chart 
        ptr2=component_data['start-col']+1
        while(ptr2<len(component_data['data'][0])+component_data['start-col']):
            chart2.add_series(
                {
                    "name":f"='{ws.name}'!${chr(ptr2+64)}${component_data['start-row']}",
                    "categories":f"='{ws.name}'!${chr(component_data['start-col']+64)}${component_data['start-row']+1}:${chr(component_data['start-col']+64)}${len(component_data['data'])+component_data['start-row']-1}",
                    "values":f"='{ws.name}'!${chr(ptr2+64)}${component_data['start-row']+1}:${chr(ptr2+64)}${len(component_data['data'])+component_data['start-row']-1}",
                }
            )
            ptr2+=1
        chart1.combine(chart2)
        if 'width' in component_data:
            chart1.set_size({'width':component_data['width']*0.36*96,'height':component_data['height']*0.388*96})
            if lastColumnOfChart(component_data['width']*0.36*96,component_data['chart-position'])>=component_data['start-col'] and ord(component_data['chart-position'][0])<component_data['start-col']+64:
                ws.set_column_pixels(component_data['start-col']-2,component_data['start-col']-2,558)
        chart1.set_title({"name":component_data['chart-title'],'name_font':{'color':'black'}})
        chart1.set_x_axis({"name": component_data['x-axis-title'],"date_axis":True,'num_font':  {'rotation': -90}})
        chart1.set_y_axis({"name": component_data['y-axis-title']})
        chart1.set_legend({'none': True})
        ws.insert_chart(component_data['chart-position'], chart1)


    def add_heatmap_data(self, ws, component_data):
        title = component_data.get('title')
        start_row = component_data.get('start-row', 0) + ExcelWriter.ROW_START
        start_col = component_data.get('start-col', 0)
        raw_data = component_data.get('data', [])

        # Convert data to dictionary format
        data_dict = {}

        # Process arrays of [timestamp, value] pairs directly from raw_data
        if isinstance(raw_data, list) and len(raw_data) > 0:
            for item in raw_data:
                if isinstance(item, list) and len(item) == 2:
                    timestamp_str, value = item
                    # Skip header row and "No data found" special case
                    if timestamp_str in ["Timestamp", "No data found"]:
                        continue
                    data_dict[timestamp_str] = value

        # Handle no data case - either empty input or no valid data entries
        if not data_dict:
            # Enhanced title format for better visibility
            title_format = self.wb.add_format({
                'bold': True,
                'font_size': 14,  # Increased font size
                'font_color': '#00598B',
                'bottom': 1,  # Add a bottom border
                'bottom_color': '#CCCCCC'  # Light gray border
            })

            # Add title with more prominence
            ws.set_row(start_row, 25)  # Increase the row height for the title
            ws.merge_range(start_row, start_col, start_row, start_col + 4, "", None)
            ws.write_string(start_row, start_col, title, title_format)

            # Add "No data found" message with more visible formatting
            no_data_format = self.wb.add_format({
                'font_size': 12,
                'align': 'left',
                'valign': 'vcenter',
                'border': 0
            })

            # Set row height for the "No data found" row
            ws.set_row(start_row + 1, 30)  # Set row height to 30 points

            # Merge cells across a wider range for the "No data found" message
            ws.merge_range(start_row + 1, start_col, start_row + 1, start_col + 4, "No data found", no_data_format)

            # Add an empty row after the "No data found" message for spacing
            ws.set_row(start_row + 1, 20)  # Add spacing to the row below

            return

        # Define formats
        title_format = self.wb.add_format({
            'bold': True,
            'font_size': 13,
            'font_color': '#00598B',
        })

        header_format = self.wb.add_format({
            'bold': True,
            'font_size': 12,
            'align': 'center',
            'border': 1,
            'border_color': '#E0E0E0',  # Light gray border
            'bg_color': '#F8F9FA'  # Very light background for headers
        })

        date_format = self.wb.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'border_color': '#E0E0E0',  # Light gray border
            'bg_color': '#F8F9FA'  # Very light background for headers
        })

        cell_format = self.wb.add_format({
            'border': 1,
            'border_color': '#E0E0E0'  # Light gray border
        })

        # Convert timestamp data to heatmap format
        heatmap_data = self._prepare_heatmap_data(data_dict)

        # Add title to the heatmap
        ws.merge_range(start_row, start_col, start_row, start_col + 48, "", title_format)
        ws.write_string(start_row, start_col, title, title_format)

        # Start with data rows
        row = start_row + 1
        date_column = start_col

        # Get all dates from the heatmap data in proper chronological order
        # The year information should be embedded in the raw_data component_data

        # First, create a mapping from display dates (like "Dec 07") to full dates with year
        date_to_full_date = {}

        # Process raw data to extract date and year information
        for item in raw_data:
            if isinstance(item, list) and len(item) == 2:
                timestamp_str, _ = item
                if timestamp_str == "Timestamp":  # Skip header
                    continue

                try:
                    # Parse the full timestamp which includes year
                    dt = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %I:%M %p')
                    display_date = dt.strftime('%b %d')  # e.g., "Dec 07"
                    full_date = dt.strftime('%Y-%m-%d')  # e.g., "2024-12-07"

                    # Store the mapping from display date to full date
                    date_to_full_date[display_date] = full_date
                except ValueError:
                    # Skip unparseable dates
                    continue

        # Sort the dates by their full date representation (with year)
        # This ensures proper chronological order across year boundaries
        dates = sorted(heatmap_data.keys(),
                      key=lambda x: date_to_full_date.get(x, '9999-99-99'),  # Default to far future if not found
                      reverse=True)  # Newest dates first

        # Write data rows
        for i, date in enumerate(dates):
            hours_data = heatmap_data[date]

            # Set the row height to create larger cells
            ws.set_row(row + i, 24)  # Increased row height for better heatmap visibility

            # Write the date at the left
            ws.write(row + i, date_column, date, date_format)

            # Write cell values with visible text (for all 48 slots - 30-minute intervals)
            for slot, value in enumerate(hours_data):
                if value is not None:
                    # Create cell format that allows values to show
                    value_format = self.wb.add_format({
                        'font_size': 12,
                        'align': 'center',
                        'border': 1,  # Light border
                        'border_color': '#E0E0E0'  # Light gray border
                    })
                    # Format the value - show as integer if it's a whole number
                    display_value = int(float(value)) if float(value) == int(float(value)) else round(float(value), 2)
                    # Write directly to the slot column
                    ws.write_number(row + i, slot + date_column + 1, float(value), value_format)
                else:
                    # Create a specific format for empty/no-data cells with white background
                    empty_cell_format = self.wb.add_format({
                        'bg_color': '#FFFFFF',  # Explicit white background for no data
                        'border': 1,  # Light border
                        'border_color': '#E0E0E0'  # Light gray border
                    })
                    # Write directly to the slot column
                    ws.write_blank(row + i, slot + date_column + 1, None, empty_cell_format)

        # Move to next row after all dates
        row = start_row + 1 + len(dates)

        # Apply conditional formatting to all data rows
        if dates:  # Only if we have data rows
            # Finding min and max values to establish proper ranges
            min_val = float('inf')
            max_val = float('-inf')

            # Use the chronologically sorted dates list we created above
            for date in dates:
                hours_data = heatmap_data[date]
                for value in hours_data:
                    if value is not None:
                        min_val = min(min_val, float(value))
                        max_val = max(max_val, float(value))

            # Set min value to 0 only if all values are the same
            if min_val == max_val:
                min_val = 0

            # Calculate range intervals for better color distribution
            value_range = max_val - min_val if max_val > min_val else 1
            step = value_range / 4  # Divide into 4 segments for 4 color ranges

            # Get the number of slots from metadata
            num_slots = getattr(self, '_heatmap_metadata', {'num_slots': 48})['num_slots']

            # First add a conditional format for blank cells - to ensure they're white
            ws.conditional_format(start_row + 1, date_column + 1, start_row + len(dates), date_column + num_slots, {
                'type': 'blanks',
                'format': self.wb.add_format({
                    'bg_color': '#FFFFFF',  # White background for empty cells
                    'border': 1,  # Light border
                    'border_color': '#E0E0E0'  # Light gray border
                })
            })

            # Now add conditional formatting for cells with values
            ws.conditional_format(start_row + 1, date_column + 1, start_row + len(dates), date_column + num_slots, {
                'type': 'cell',
                'criteria': '<',
                'value': min_val + step,
                'format': self.wb.add_format({
                    'bg_color': '#EBF0FD',  # Lightest blue
                    'border': 1,  # Light border
                    'border_color': '#E0E0E0'  # Light gray border
                })
            })

            ws.conditional_format(start_row + 1, date_column + 1, start_row + len(dates), date_column + num_slots, {
                'type': 'cell',
                'criteria': 'between',
                'minimum': min_val + step,
                'maximum': min_val + 2*step,
                'format': self.wb.add_format({
                    'bg_color': '#C7D2F9',  # Light blue
                    'border': 1,  # Light border
                    'border_color': '#E0E0E0'  # Light gray border
                })
            })

            ws.conditional_format(start_row + 1, date_column + 1, start_row + len(dates), date_column + num_slots, {
                'type': 'cell',
                'criteria': 'between',
                'minimum': min_val + 2*step,
                'maximum': min_val + 3*step,
                'format': self.wb.add_format({
                    'bg_color': '#7388F4',  # Medium blue
                    'border': 1,  # Light border
                    'border_color': '#E0E0E0'  # Light gray border
                })
            })

            ws.conditional_format(start_row + 1, date_column + 1, start_row + len(dates), date_column + num_slots, {
                'type': 'cell',
                'criteria': '>=',
                'value': min_val + 3*step,
                'format': self.wb.add_format({
                    'bg_color': '#1C64F2',  # Dark blue (100%)
                    'border': 1,  # Light border
                    'border_color': '#E0E0E0'  # Light gray border
                })
            })

        # Write time headers at the bottom
        ws.write(row, date_column, "Time", header_format)

        # Get the metadata from the _prepare_heatmap_data method
        metadata = getattr(self, '_heatmap_metadata', {'num_slots': 24})
        num_slots = metadata['num_slots']

        # Write time headers with hours only (no minutes)
        for slot_idx in range(num_slots):
            hour = slot_idx

            period = "AM" if hour < 12 else "PM"
            display_hour = hour % 12
            if display_hour == 0:
                display_hour = 12

            # Format time header with just hours (no minutes)
            time_header = f"{display_hour} {period}"
            ws.write(row, slot_idx + date_column + 1, time_header, header_format)

        row += 1

        # Add an empty row for spacing between chart and range bar
        row += 1

        # Add value range legend
        if dates:  # Only if we have data rows
            # Find min and max values
            min_val = float('inf')
            max_val = float('-inf')

            # Use the chronologically sorted dates list we created above
            for date in dates:
                hours_data = heatmap_data[date]
                for value in hours_data:
                    if value is not None:
                        min_val = min(min_val, float(value))
                        max_val = max(max_val, float(value))

            # Set min value to 0 only if all values are the same
            if min_val == max_val:
                min_val = 0

            # Preserve original values without rounding for accurate representation
            # We'll handle the display formatting later
            min_val = float(min_val)
            max_val = float(max_val)

            # Create legend format
            legend_format = self.wb.add_format({
                'font_size': 10,
                'align': 'center'
            })

            # Add gradient bar and values
            gradient_width = 4  # Number of cells to use for the gradient (one per color)

            # Colors matching the screenshot exactly
            colors = [
                '#EBF0FD',    # Lightest blue
                '#C7D2F9',    # Light blue
                '#7388F4',    # Medium blue
                '#1C64F2',    # Dark blue (100%)
                '#FFFFFF'     # White for empty cells (not shown in gradient)
            ]

            # Directly use the specific colors - one color per cell
            for i in range(gradient_width):
                # Use each color exactly once (colors 0-3)
                cell_format = self.wb.add_format({
                    'bg_color': colors[i],
                    'border': 0
                })

                ws.write_blank(row, date_column + 1 + i, None, cell_format)

            # Add min and max values, ensuring we use actual values from the data
            # Only show min_val if it exists in the data, otherwise show 0
            display_min = min_val if min_val != float('inf') else 0
            display_max = max_val if max_val != float('-inf') else 0

            # Format numbers with consistent decimal display
            # For integers (whole numbers), show as integers
            # For decimals, always show exactly 2 decimal places
            if display_min == int(display_min):
                display_min_str = str(int(display_min))
            else:
                display_min_str = f"{display_min:.2f}"  # Always show 2 decimal places

            if display_max == int(display_max):
                display_max_str = str(int(display_max))
            else:
                display_max_str = f"{display_max:.2f}"  # Always show 2 decimal places

            ws.write(row, date_column, display_min_str, legend_format)
            ws.write(row, date_column + 1 + gradient_width, display_max_str, legend_format)

        # Set column widths based on the number of slots
        num_slots = getattr(self, '_heatmap_metadata', {'num_slots': 48})['num_slots']
        ws.set_column(date_column, date_column, 15)   # Date column - increased from 12 to 15
        ws.set_column(date_column + 1, date_column + num_slots, 10)   # Time columns with width adjusted to fit time format

    def _prepare_heatmap_data(self, values_dict):
        """Convert timestamp values to a date/hour heatmap structure with only hours (no minutes)"""

        # If dictionary is empty, return an empty result
        if not values_dict:
            self._heatmap_metadata = {
                'num_slots': 24  # Default to 24 slots
            }
            return {}

        # We'll use 24 slots for hourly data (one time point per hour)
        num_slots = 24

        # Create the heatmap structure - defaultdict with None values for each hour slot
        heatmap = defaultdict(lambda: [None] * num_slots)

        # Process each timestamp and map it to the appropriate hour slot
        parsed = []
        for ts_str, val_str in values_dict.items():
            try:
                # Parse the timestamp
                try:
                    dt = datetime.datetime.strptime(ts_str, '%Y-%m-%d %I:%M %p')
                except ValueError:
                    # Try unix timestamp as fallback
                    try:
                        ts = int(float(ts_str))
                        dt = datetime.datetime.fromtimestamp(ts)
                    except (ValueError, TypeError):
                        print(f"Error processing timestamp {ts_str}: unparseable format")
                        continue

                # Extract date components and hour value for slot mapping
                date_str = dt.strftime('%b %d')  # e.g., "Dec 07"
                hour_value = dt.hour  # Use just the hour part for mapping
                full_date_str = dt.strftime("%Y-%m-%d")  # Keep full date with year for sorting
                val = float(val_str)

                # Store the year info directly with the display date for better sorting later
                year = dt.year
                # Create a special sorting key that includes the year
                sort_key = f"{year}{date_str}"

                parsed.append((date_str, hour_value, val, full_date_str, sort_key, year))
            except Exception as e:
                print(f"Error processing timestamp {ts_str}: {e}")
                continue

        # Extract date information with years for proper sorting
        date_with_year_info = {}
        for date_str, _, _, full_date, sort_key, year in parsed:
            date_with_year_info[date_str] = (full_date, sort_key, year)

        # Get unique days with proper chronological sorting (newest to oldest)
        # Sort by the full date with year information
        days = sorted({d for d, _, _, _, _, _ in parsed},
                     key=lambda x: date_with_year_info[x][0],  # Use full ISO date (YYYY-MM-DD)
                     reverse=True)  # Newest dates first

        # Build the heatmap - map data to hourly slots
        for date_str in days:
            for hour_idx in range(24):  # All 24 hours
                # Find matching data for this day and hour
                match = [v for d, h, v, _, _, _ in parsed if d == date_str and h == hour_idx]
                if match:
                    # If multiple values exist for the same hour (different minutes), use the first one
                    heatmap[date_str][hour_idx] = match[0]

        # Store metadata for use by the caller - just store number of slots now
        self._heatmap_metadata = {
            'num_slots': num_slots
        }

        return heatmap






    def add_insights_table(self, ws, component_data):
        # Extract starting row and column
        row_start = component_data['start-row'] + ExcelWriter.ROW_START + 1  # Adjust for 1-based indexing
        col_start = component_data['start-col']

        # Add table title if provided
        if 'title' in component_data:
            title_format = self.wb.add_format({'bold': True, 'font_color': '#00598B'})
            ws.write(row_start - 1, col_start, component_data['title'], title_format)

        # Handle single value as table data
        if isinstance(component_data['data'], (int, float, str)):
            ws.write(row_start, col_start, component_data['data'])
            col_width = len(str(component_data['data']))
            ws.set_column(col_start, col_start, col_width + 2)
        else:
            col_widths = [len(str(header)) for header in component_data['data'][0]]  # Start with header row
            for row in component_data['data']:
                col_widths = [max(col_widths[i], len(str(item))) for i, item in enumerate(row)]

            col_widths = [width + 2 for width in col_widths]  # Add padding

            for col_idx, width in enumerate(col_widths):
                ws.set_column(col_start + col_idx, col_start + col_idx, width)

            header_format = self.wb.add_format({'bold': True, 'bg_color': '#5884be', 'align': 'left', 'font_color': 'white', 'border': 1, 'border_color': '#FFFFFF'}) #4F81BD
            for col_idx, header in enumerate(component_data['data'][0]):
                ws.write(row_start, col_start + col_idx, header, header_format)

            row_format_odd = self.wb.add_format({'bg_color': '#B8CCE4', 'align': 'left', 'border': 1, 'border_color': '#FFFFFF'})  # Light gray
            row_format_even = self.wb.add_format({'bg_color': '#DCE6F1', 'align': 'left', 'border': 1, 'border_color': '#FFFFFF'})  # White

            for row_idx, row_data in enumerate(component_data['data'][1:], start=1):  # Skip header row
                current_format = row_format_odd if row_idx % 2 == 1 else row_format_even
                for col_idx, value in enumerate(row_data):
                    ws.write(row_start + row_idx, col_start + col_idx, value, current_format)


    def add_component_title(self, ws, component_data):
        """
        add component title
        """
        if 'title' in component_data and component_data['title'] is not None and len(component_data['title']) > 0:
            cell_position = xlsxwriter.utility.xl_rowcol_to_cell(component_data['start-row'], component_data['start-col'])
            ws.write(cell_position, component_data['title'], self.wb.add_format({'bold': True, 'font_color':'#00598B'}))


    def _add_component_title(self, ws, component_data):
        color = component_data.get('title-color', '#00598B')  # Default color if not provided
        title_format = self.wb.add_format({'font_color': f'{color}', 'bold': True})
        ws.write(component_data['start-row'] - 1, component_data['start-col'] - 1, component_data['_title'], self.wb.add_format({'font_color': f'{color}', 'bold': True}))  # Adjust for 0-based index
        # ws = self.wb.add_worksheet()


    def _set_title_as_header(self, ws, sheet_data):
        header_format = self.wb.add_format({'bold': True, 'font_color': '#00598B', 'align': 'left', 'valign': 'vcleft', 'font_size': 13, # 'bg_color': '#eeeeee'
            })
        row_format = self.wb.add_format({'bg_color': '#eeeeee'     # Row background fill color
        })

        for row_idx in range(1):  # 0-based indexing; 'ROW_START - 1'
            ws.set_row(row_idx, None, row_format)  # Set row format
        ws.merge_range('A1:RR2', sheet_data['tab-title-header'].replace('_', ' ').title(), header_format)


    def add_component(self, ws, component_data, title):
        if component_data:
            if 'type' in component_data:
                if component_data['type'] == 'name':
                    if 'title' in component_data and component_data.get('title'):
                        self.add_component_title(ws, component_data)
                    elif '_title' in component_data and component_data.get('_title'):
                        self._add_component_title(ws, component_data)
                if component_data['type'] == 'table' and 'is-insights-type-table' in component_data and component_data['is-insights-type-table'] and component_data['is-insights-type-table'] == True:
                    self.add_insights_table(ws, component_data)
                elif component_data['type'] == 'table':
                    if title:
                        start_row = 1
                        start_col = 1
                        if 'data' in component_data and len(component_data['data']) > 0:
                            headers = component_data['data'][0:1]
                            data = component_data['data'][1:len(component_data['data'])]
                        if 'start-row' in component_data and 'start-col' in component_data:
                            start_row = component_data['start-row']
                            start_col = component_data['start-col']
                        # if 'title' in component_data and component_data.get('title'):
                        #     self.add_component_title(ws, component_data)
                        if 'metric_sheet' in component_data and component_data['metric_sheet'] == True:
                            headers = component_data['data'][0:2]
                            data = component_data['data'][2:len(component_data['data'])]
                            self.render_metric_table(ws, component_data, component_data['merge_cells'], title, headers, data, start_row, start_col)
                        # elif 'is-insights-type-table' in component_data and component_data['is-insights-type-table'] and component_data['is-insights-type-table'] == True:
                        #     self.add_table(ws, component_data)
                        else:
                            self.render_table(ws, title, headers, data, start_row, start_col)
                elif component_data['type']=='doughnut-chart':
                    self.add_doughnut_chart(ws,component_data)
                elif component_data['type']=='pie-chart':
                    self.add_pie_chart(ws,component_data) 
                elif component_data['type']=='scatter-chart':    
                    self.add_scatter_chart(ws,component_data)
                elif component_data['type']=='bar-chart':
                    self.add_bar_chart(ws,component_data) 
                elif component_data['type']=='line-chart':
                    self.add_line_chart(ws,component_data)
                elif component_data['type']=='stack-bar-chart':
                    self.add_stack_bar_chart(ws,component_data)
                elif component_data['type']=='bar-line-trend-chart':
                    self.add_bar_line_trend_chart(ws,component_data)
                elif component_data['type']=='heatmap-table':
                    self.add_heatmap_data(ws,component_data)


    def render(self, excel_data):
        if excel_data:
            for sheet in excel_data['sheets']:
                if (('title' in sheet and len(sheet['title']) > 0 and sheet['title'].lower() == 'summary') or ('summary' in sheet and sheet['summary'] == 'true')):
                    self.write_summary_data(sheet['data'])
                elif 'documentation' in sheet and sheet['documentation'] == 'true':
                    self.write_glossary_data(sheet['data'])
                else:
                    title = None
                    if 'title' in sheet:
                        title = sheet['title']
                    if title is None or len(title) <= 0:
                        if 'title' in component_data and component_data['title'] is not None and len(component_data['title']) > 0:
                            title = component_data['title']
                    ws = self.create_sheet(title)

                    if 'tab-title-header' in sheet:
                        self._set_title_as_header(ws, sheet)

                    for component_data in sheet['components']:
                        self.add_component(ws, component_data, title)