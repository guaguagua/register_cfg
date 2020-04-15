import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox,QTableWidgetItem,QComboBox,QAbstractItemView
from json_parse import RegisterJson
from ui_register import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
import json
 

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        #print("__init__")
        super(MainWindow, self).__init__(parent)
        
        self.json_parse = RegisterJson("./register.json")
        self.default_addr = "0x00000000"
        '''
        for addr in self.json_parse.cfg_addr_list:
            if addr != self.default_addr:
                self.default_addr = addr
                break'''
        self.data_bit_len = self.json_parse.data_byte_len * 8

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.check_btn_list = [ self.ui.check_32_0,self.ui.check_32_1,self.ui.check_32_2,self.ui.check_32_3,
                                self.ui.check_32_4,self.ui.check_32_5,self.ui.check_32_6,self.ui.check_32_7,
                                self.ui.check_32_8,self.ui.check_32_9,self.ui.check_32_10,self.ui.check_32_11,
                                self.ui.check_32_12,self.ui.check_32_13,self.ui.check_32_14,self.ui.check_32_15,
                                self.ui.check_32_16,self.ui.check_32_17,self.ui.check_32_18,self.ui.check_32_19,
                                self.ui.check_32_20,self.ui.check_32_21,self.ui.check_32_22,self.ui.check_32_23,
                                self.ui.check_32_24,self.ui.check_32_25,self.ui.check_32_26,self.ui.check_32_27,
                                self.ui.check_32_28,self.ui.check_32_29,self.ui.check_32_30,self.ui.check_32_31]

        self.table_com_box_list = []
        
        self.init_all_check_bit_btn()
        self.init_table()
        
        #触发一下地址信息改变
        self.send_addr_change_signal()  

        self.init_cfg()

        self.ui.hex_update_value_enable_radio.setChecked(True)
        

    # common use########################################################################
    def send_addr_change_signal(self):
        #cur_addr = self.ui.hex_line_edit_addr.text()
        #self.ui.hex_line_edit_addr.setText("0x00000000")#发送信号
        self.ui.hex_line_edit_addr.setText("0xFFFFFFFF")    
        self.ui.hex_line_edit_addr.setText(self.default_addr)
        #print("cur_addr",cur_addr)

    def reload_all_json_data(self):
        self.json_parse = RegisterJson("./register.json")
        #self.ui.hex_line_edit_addr.setText(self.default_addr)
        #print(self.default_addr)
        #self.send_addr_change_signal()

    # addr handle functions########################################################################
    @pyqtSlot('QString')# @pyqtSlot(str),@pyqtSlot(int)
    def on_hex_line_edit_addr_textChanged(self,addr):
        #print("on_hex_line_edit_addr_textChanged")
        if len(addr) != len(self.default_addr):
            return
        self.update_addr_value()
        #self.update_reset_value()
        self.update_table(addr)
        
    @pyqtSlot()
    def on_hex_addr_up_clicked(self):
        #print("on_hex_addr_up_clicked")
        addr = self.ui.hex_line_edit_addr.text()
        addr = int(addr,16) + 4
        addr = self.json_parse.trans_addr_to_json(hex(addr))
        self.ui.hex_line_edit_addr.setText(addr)

    @pyqtSlot()
    def on_hex_addr_down_clicked(self):
        #print("on_hex_addr_down_clicked")
        addr = self.ui.hex_line_edit_addr.text()
        addr = int(addr,16) - 4
        if addr < 0:
            addr = 0
        addr = self.json_parse.trans_addr_to_json(hex(addr))
        self.ui.hex_line_edit_addr.setText(addr)
    
    @pyqtSlot()
    def on_hex_reload_btn_clicked(self):
        self.reload_all_json_data()
        self.update_addr_value()

    def update_addr_value(self):
        addr = self.ui.hex_line_edit_addr.text()

        value = self.json_parse.get_addr_value(addr)
        if not value:
            #reply = QMessageBox.information(self,"msg","addr value not exists",QMessageBox.Yes)
            self.ui.hex_addr_cfg_tip.setText("Not find config")
            self.ui.hex_addr_cfg_tip.setStyleSheet("color: red")
            return
        else:
            self.ui.hex_line_edit_value.setText(value)

        value = self.json_parse.get_reset_value(addr)
        if not value:
            #reply = QMessageBox.information(self,"msg","addr reset value not exists",QMessageBox.Yes)
            self.ui.hex_addr_cfg_tip.setText("Not find config")
            self.ui.hex_addr_cfg_tip.setStyleSheet("color: red")
            return
        else:
            self.ui.hex_line_edit_reset_value.setText(value)

        self.ui.hex_addr_cfg_tip.setText(" "*15)

    # value handle functions########################################################################
    @pyqtSlot(str)#self.lineEdit.returnPressed.connect(self.lineEdit_function)
    def on_hex_line_edit_value_textChanged(self,value):
        #self.on_hex_line_edit_addr_textChanged(value)
        #print("on_hex_line_edit_value_textChanged")
        #print(value)
        if len(value) != len(self.default_addr):
            return
        self.update_all_check_btn() #更新Bit表

        #update table
        addr = self.ui.hex_line_edit_addr.text()
        self.update_table(addr) 
        #self.ui.hex_update_value_enable_radio.setChecked(True)
    
    @pyqtSlot(bool)
    def on_hex_update_value_enable_radio_toggled(self,bool):
        print("on_hex_update_value_enable_radio_toggled")
        self.update_all_check_btn()
        addr = self.ui.hex_line_edit_addr.text()
        self.update_table(addr)

    @pyqtSlot()
    def on_hex_save_btn_clicked(self):
        #print("on_hex_save_btn_clicked")
        #save to regiter_cfg.json
        addr = self.ui.hex_line_edit_addr.text()
        addr = self.json_parse.trans_addr_to_json(addr)

        if True:
            value = self.ui.hex_line_edit_value.text()
            value = self.json_parse.trans_addr_to_json(value)
            if addr in self.json_parse.cfg_addr_list:
                #print("cfg_addr_list")
                self.json_parse.json_reg_cfg_data[addr]["value"] = value
                #self.json_parse.write_json(self.json_parse.json_reg_cfg_data,self.json_parse.register_cfg_file_path)
            else:# add new addr config
                #print("cfg_addr_list else")
                self.json_parse.json_reg_cfg_data[addr] = {}
                self.json_parse.json_reg_cfg_data[addr]["value"] = value
                self.json_parse.json_reg_cfg_data[addr]["bit_len"] = "32"
                self.json_parse.json_reg_cfg_data[addr]["region"] = []
            
            if addr in self.json_parse.value_addr_list:#save to register_value.json
                #print("value_addr_list")
                print("replace tip")
                self.json_parse.json_reg_value_data[addr] = value

        if True:
            value = self.ui.hex_line_edit_reset_value.text()
            if addr in self.json_parse.cfg_addr_list:
                self.json_parse.json_reg_cfg_data[addr]["reset_value"] = value

        self.json_parse.save_all_data()
        #print("88888888888888888888888888888")

    # reset value handle ########################################################################
    @pyqtSlot(str)
    def on_hex_line_edit_reset_value_textChanged(self,value):
        #print("on_hex_line_edit_reset_value_textChanged")
        if len(value) != len(self.default_addr):
            return
        self.update_all_check_btn() #更新Bit表

        #update table
        addr = self.ui.hex_line_edit_addr.text()
        self.update_table(addr)

    #bit handle functions############################################################################
    def init_all_check_bit_btn(self):
        self.ui.hex_bit_edit_check.setChecked(True)
        self.ui.hex_bit_edit_check.setChecked(False)
        self.connect_all_check_btn()
        #self.update_bit_check_color(0,0,0)

    def connect_all_check_btn(self):
        for check in self.check_btn_list:
            #self.base_doubleSpinBox.valueChanged['double'].connect(MainWindow.getResult)
            check.toggled['bool'].connect(self.update_hex_line_edit_value)

    def update_all_check_btn(self):
        if self.ui.hex_update_value_enable_radio.isChecked():
            text = self.ui.hex_line_edit_value.text()
        elif self.ui.hex_update_reset_enable_radio.isChecked():
            text = self.ui.hex_line_edit_reset_value.text()
        else:
            #print("update_all_check_btn error")
            return
        value = int(text,16)

        data_bit_len = self.json_parse.data_byte_len * 8
        for i in range(0,data_bit_len):
            if self.get_bit(value,i):
                self.check_btn_list[i].setChecked(True)
            else:
                self.check_btn_list[i].setChecked(False)

    def update_hex_line_edit_value(self):
        #print("update_hex_line_edit_value")
        data_bit_len = self.json_parse.data_byte_len * 8
        value = 0x00000000;
        for i in range(0,data_bit_len):
            if self.check_btn_list[i].isChecked():
                value = self.set_bit(value,i)
            else:
                value = self.clear_bit(value,i)
        value = self.json_parse.trans_addr_to_json(hex(value))
        if self.ui.hex_update_value_enable_radio.isChecked():#11111
            self.ui.hex_line_edit_value.setText(value)
        else:
            self.ui.hex_line_edit_reset_value.setText(value)

    def set_all_bit_check_state(self,state):
        for box in self.check_btn_list:
            box.setEnabled(state)
    
    def update_bit_check_color(self,start,end,color):
        self.check_btn_list[0].setStyleSheet("background: red")
        #self.check_btn_list[0].setStyleSheet("color: red")
        pass

    @pyqtSlot(bool)
    def on_hex_bit_edit_check_toggled(self,bool):
        #print(bool)
        self.set_all_bit_check_state(bool)
        self.ui.hex_bit_clear_all_btn.setEnabled(bool)
        self.ui.hex_bit_set_all_btn.setEnabled(bool)

    @pyqtSlot()
    def on_hex_bit_clear_all_btn_clicked(self):
        self.check_btn_list[0].setChecked(True)#保证在全0全1的时候会触发一下toggle事件
        for i in range(self.data_bit_len):#32bit
            self.check_btn_list[i].setChecked(False)
    @pyqtSlot()
    def on_hex_bit_set_all_btn_clicked(self):
        self.check_btn_list[0].setChecked(False)#保证在全0全1的时候会触发一下toggle事件
        for i in range(self.data_bit_len):#32bit
            self.check_btn_list[i].setChecked(True)

    def set_bit(self,value,bit):
        value = value | (1 << bit )
        return value
    
    def get_bit(self,value,bit):
        if value & ( 1 << bit ):
            return 1
        return 0

    def clear_bit(self,value,bit):
        value = value & (~(1 << bit))
        return value

    #table handle##################################################################
    def init_table(self):
        #header = ["feild","bit-range","value(hex)","func-list"]
        self.table_feild_col = 0
        self.table_range_col = 1
        self.table_value_col = 2
        self.table_func_col  = 3

        self.table_set_header()
        #addr = self.ui.hex_line_edit_addr.text()
        self.ui.hex_line_edit_addr.setText(self.default_addr)
        print(self.default_addr)
        self.ui.hex_table_edit_check.setChecked(False)
        self.ui.hex_table_update_btn.setEnabled(False)

        self.update_table(self.default_addr)
        self.set_table_com_box_state(False)
        
        self.ui.hex_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    @pyqtSlot(bool)
    def on_hex_table_edit_check_toggled(self,bool):
        self.set_table_com_box_state(bool)
        self.ui.hex_table_update_btn.setEnabled(bool)

    @pyqtSlot()
    def on_hex_table_update_btn_clicked(self):
        #update value
        addr = self.ui.hex_line_edit_addr.text()
        row = len( self.json_parse.json_reg_cfg_data[addr]["region"] )
        sum_value = 0
        print("row",row)
        for i in range(row):
            str_bit = self.ui.hex_table.item(i,1).text()
            start_bit = str_bit.split("-")[0]
            end_bit   = str_bit.split("-")[1]
            start_bit = int(start_bit)
            end_bit   = int(end_bit)

            text = self.ui.hex_table.item(i,self.table_value_col).text()
            value = int(text,16) << start_bit 
            print(text,hex(value),start_bit)
            sum_value |= value
        sum_value = self.json_parse.trans_addr_to_json(hex(sum_value))
        print("sum_value",sum_value)

        if self.ui.hex_update_value_enable_radio.isChecked():#11111
            self.ui.hex_line_edit_value.setText(sum_value)
        else:
            self.ui.hex_line_edit_reset_value.setText(sum_value)
            #self.update_all_check_btn() #更新Bit表

    def set_table_com_box_state(self,state):
        for box in self.table_com_box_list:
            #box.setEditable(state)
            box.setEnabled(state)
            #print("set_table_com_box_state",state)

    def get_bit_range_value(self,value,start_bit,end_bit):
        bit_len = end_bit - start_bit + 1
        return (value >> start_bit) & (( 1 << bit_len)-1 )
    
    def clear_table_combo_box(self):
        for box in self.table_com_box_list:#断开之前的链接
            #print("disconnect",box.objectName())
            box.currentTextChanged.disconnect(self.table_combo_box_change_handle)

        self.table_com_box_list = []

    def table_set_header(self):
        header = ["feild","bit-range","value(hex)","func-list"]
        self.ui.hex_table.setHorizontalHeaderLabels(header)

    def clear_table(self):
        self.ui.hex_table.clear()#clear会把表头清楚，所以需要重新设置下
        self.clear_table_combo_box()
        self.table_set_header()

    def update_table_name(self,row,col,name):
        self.ui.hex_table.setItem(row,col,QTableWidgetItem(name))

    def update_table_range(self,row,col,range_bit):
        self.ui.hex_table.setItem(row,col,QTableWidgetItem(range_bit))

    def update_table_value(self,row,col,value):
        self.ui.hex_table.setItem(row,col,QTableWidgetItem(value))

    def update_table_func(self,row,col,func):
        self.ui.hex_table.setItem(row,col,QTableWidgetItem(func))

    def update_table_all_func(self,row,col,func_list):
        #self.clear_table_combo_box()

        com_box = QComboBox(self)
        com_box.setObjectName("table_com_box_"+str(row))
        com_box.currentTextChanged.connect(self.table_combo_box_change_handle)
        self.table_com_box_list.append(com_box)
        for func in func_list:
            com_box.addItem(func)
        self.ui.hex_table.setCellWidget(row,col,com_box)

    def update_table(self,addr):#通过ddr 重新获取需要展示到表格的数据
        self.clear_table()

        if addr not in self.json_parse.cfg_addr_list:
            return
        
        region_list = self.json_parse.json_reg_cfg_data[addr]["region"]
        if 0 == len(region_list):
            self.ui.hex_table_func_list_label.setText("No func config")
            self.ui.hex_table_func_list_label.setStyleSheet("color: red")
        else:
            self.ui.hex_table_func_list_label.setText(" "*len("No func config"))

        value = 0
        if self.ui.hex_update_value_enable_radio.isChecked():
            value = self.ui.hex_line_edit_value.text()
        elif self.ui.hex_update_reset_enable_radio.isChecked():
            value = self.ui.hex_line_edit_reset_value.text()
            #print("update_table reset")
        else:
            print("update_table error")
            return
        value = int(value,16)

        for row in range(len(region_list)):
            d = region_list[row]
            name = d["name"]
            bit_start = d["start"]
            bit_end = d["end"]
            bit_range =  bit_start + "-" + bit_end
            dic_func = d["func"]

            self.update_table_name(row,self.table_feild_col,name)
            self.update_table_range(row,self.table_range_col,bit_range)

            cell_value = self.get_bit_range_value(value,int(bit_start),int(bit_end))
            cell_value = self.json_parse.trans_addr_to_json(hex(cell_value))
            self.update_table_value(row,self.table_value_col,cell_value)
            
            dic_func_list = list(dic_func.values())
            dic_func_list.append("Not Found")
            self.update_table_all_func(row,self.table_func_col,dic_func_list)

            key = cell_value
            if key in dic_func:
                self.table_com_box_list[row].setCurrentText(dic_func[key])
            else:
                self.table_com_box_list[row].setCurrentText("Not Found")

        if self.ui.hex_table_edit_check.checkState():
            self.set_table_com_box_state(True)
        else:
            self.set_table_com_box_state(False)

    def table_combo_box_change_handle(self,func):
        #print("*"*50)
        sender = self.sender()
        #print(func)
        if not self.ui.hex_table_edit_check.checkState():#表格编辑没有使能
            return
        
        if not sender.objectName().startswith("table_com_box_"):#这里应该有bug:hex_line_edit_addr 改变也会触发，实际并没有connect到hex_line_edit_addr
            #print("&"*50,sender.objectName())
            return

        if "Not Found" == func:
            #msg: can not select this func
            #currentText = sender.currentText()
            #print(currentText)
            reply = QMessageBox.information(self,"msg","can not select this func",QMessageBox.Yes)
            return
        
        #查找func对应的值
        addr = self.ui.hex_line_edit_addr.text()
        table_line = int( sender.objectName()[14:] ) # 14 = start = len("table_com_box_")
        if addr in self.json_parse.cfg_addr_list:
            dic_func = self.json_parse.json_reg_cfg_data[addr]["region"][table_line]["func"]
            for k,v in dic_func.items():#k = value
                if v == func:
                    #update table value
                    table_value = k
                    self.ui.hex_table.setItem(table_line,self.table_value_col,QTableWidgetItem(table_value))

    #cfg handle##################################################################
    def init_cfg(self):
        self.ui.cfg_line_edit_addr.setText(self.default_addr)
        self.ui.cfg_add_label.setText(" "*len("json error"))
        self.ui.cfg_add_label.setStyleSheet("color: red")

    @pyqtSlot(str)
    def on_cfg_line_edit_addr_textChanged(self,addr):
        print("on_cfg_line_edit_addr_textChanged")
        #self.ui.cfg_add_label.setText(" "*len("json error"))

    def read_addr_cfg(self):
        addr = self.ui.cfg_line_edit_addr.text()
        if addr in self.json_parse.cfg_addr_list:
            addr_cfg = self.json_parse.json_reg_cfg_data[addr]
            addr_cfg = json.dumps(addr_cfg, indent=4)
            self.ui.cfg_text_edit.setText(str(addr_cfg))
        else:
            #print("on_cfg_read_btn_clicked not find addr:%s",(addr,))
            text = " not find addr:{} config".format(addr)
            self.ui.cfg_text_edit.setText(text)

        self.ui.cfg_add_label.setText(" "*len("json error"))


    @pyqtSlot()
    def on_cfg_read_btn_clicked(self):
        self.read_addr_cfg()
        #self.ui.cfg_add_label.setText(" "*len("json error"))

    @pyqtSlot()
    def on_cfg_demo_btn_clicked(self):
        with open("./cfg_demo.json","r") as f:
            text = f.read()
            self.ui.cfg_text_edit.setText(text)
            f.close()
        self.ui.cfg_add_label.setText(" "*len("json error"))

    @pyqtSlot()
    def on_cfg_clear_btn_clicked(self):
        self.ui.cfg_text_edit.setText("")
        self.ui.cfg_add_label.setText(" "*len("json error"))

    @pyqtSlot()
    def on_cfg_add_btn_clicked(self):
        text = self.ui.cfg_text_edit.toPlainText()
        self.ui.cfg_add_label.setText(" "*len("json error"))
        try:# 数据json字符串格式不符合要求
            dic = json.loads(text)
        except Exception as e:
            print(e)
            self.ui.cfg_add_label.setText("json error")
            return
        print(type(dic))
        addr = self.ui.cfg_line_edit_addr.text()
        addr = self.json_parse.trans_addr_to_json(addr)
        if addr in self.json_parse.cfg_addr_list:
            #print("repalce??")
            pass
        #print(dic)
        self.json_parse.json_reg_cfg_data[addr] = dic

        self.json_parse.json_reg_value_data[addr] = dic["value"]

        self.json_parse.save_all_data()
        #print("999999999999999999999999999999")
        #print(self.json_parse.json_reg_cfg_data[addr])

        # udate json ram data
        #self.reload_all_json_data()
        #print(self.json_parse.json_reg_cfg_data[addr])

    @pyqtSlot()
    def on_cfg_up_btn_clicked(self):
        addr = self.ui.cfg_line_edit_addr.text()
        addr = int(addr,16) + 4
        addr = self.json_parse.trans_addr_to_json(hex(addr))
        self.ui.cfg_line_edit_addr.setText(addr)

        self.read_addr_cfg()

    @pyqtSlot()
    def on_cfg_down_btn_clicked(self):
        addr = self.ui.cfg_line_edit_addr.text()
        addr = int(addr,16) - 4
        if addr < 0:
            addr = 0
        addr = self.json_parse.trans_addr_to_json(hex(addr))
        self.ui.cfg_line_edit_addr.setText(addr)

        self.read_addr_cfg()

    @pyqtSlot()
    def on_cfg_read_json_cfg_btn_clicked(self):
        with open("./register_cfg.json") as f:
            text = f.read()
            self.ui.cfg_text_edit.setText(text)
            f.close()
        self.ui.cfg_add_label.setText(" "*len("json error"))


    @pyqtSlot()
    def on_cfg_read_json_value_btn_clicked(self):
        with open("./register_value.json") as f:
            text = f.read()
            self.ui.cfg_text_edit.setText(text)
            f.close()
        self.ui.cfg_add_label.setText(" "*len("json error"))

    @pyqtSlot()
    def on_cfg_generate_reg_c_file_clicked(self):
        text = "void register_init(void)\n"
        text += "{\n"
        for k,v in self.json_parse.json_reg_value_data.items():
            #print(k,v)
            # *((volatile uint32_t*) 0x00000000) = 0x00000000;
            text += "    *((volatile uint32_t*) {}) = {}; \n".format(k,v)
        text += "}"
        self.ui.cfg_text_edit.setText(text)

        self.ui.cfg_add_label.setText(" "*len("json error"))

    @pyqtSlot()
    def on_cfg_addr_list_btn_clicked(self):
        text = ""
        for x in self.json_parse.cfg_addr_list:
            text += x+"\n"
        self.ui.cfg_text_edit.setText(text)

        self.ui.cfg_add_label.setText(" "*len("json error"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())