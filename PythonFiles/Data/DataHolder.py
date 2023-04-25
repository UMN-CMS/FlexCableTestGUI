################################################################################
import json, logging, socket, os, sys
import datetime
#sys.path.insert(0, "/home/hgcal/FlexCableTestGUI/FlexCableTestGUI/PythonFiles/Data")
#print(sys.path)
#from DBSender import DBSender
#from PythonFiles.Data.DBSender import DBSender

FORMAT = '%(asctime)s|%(levelname)s|%(message)s|'
logging.basicConfig(filename="{}/PythonFiles/logs/GUIWindow.log".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'), filemode = 'w', format=FORMAT, level=logging.DEBUG)

class DataHolder():

    #################################################

    # List of the variables being held by data holder
    def __init__(self):
        
        # Object that sends information to the database
        #self.data_sender = DBSender()
        # Commnting out everything to do with the Database. See Data directory for results and other stuff        

        self.user_path = "/home/hgcal/FlexCableTestGUI/Data/static/users.json"
        self.board_path = "/home/hgcal/FlexCableTestGUI/Data/static/boards.json"
        self.results_path = "/home/hgcal/FlexCableTestGUI/Data/results"

        self.data_dict = {
                'user_ID': "_",
                'test_stand': str(socket.gethostname()),
                'current_serial_ID': "-1BAD",
                'test1_completed': False,
                #'test2_completed': False,
                #'test3_completed': False,
                'test4_completed': False,
                'test1_pass': False,
                #'test2_pass': False,
                #'test3_pass': False,
                'test4_pass': False,
                'comments': "_",
                'is_new_board': False,
                'tests_run': [str(1), str(2), str(3), str(4)],
                #'tests_run': [str(1), str(4)],
                }
        self.inspection_data = {
                'board_chipped_bent': False,
                'wagon_connection_pin_bent': False,
                'engine_connection_pin_bent': False,
                'visual_scratches': False,
                'inspection_comments': "_"
                }
        self.data_lists = {
                'test_results': [self.data_dict['test1_pass'], self.data_dict['test4_pass']],
                'test_completion': [self.data_dict['test1_completed'], self.data_dict['test4_completed']] 
                #'test_results': [self.data_dict['test1_pass'], self.data_dict['test2_pass'], self.data_dict['test3_pass'], self.data_dict['test4_pass']],
                #'test_completion': [self.data_dict['test1_completed'], self.data_dict['test2_completed'], self.data_dict['test3_completed'], self.data_dict['test4_completed']] 
                }
    
    #################################################

    def add_new_user_name(self, user_ID, passwd):
        self.data_dict['user_ID'] = user_ID
        
        is_new_user_ID = True

        for item in self.get_all_users():
            if self.data_dict['user_ID'] == item:
                is_new_user_ID = False
        print("\n\n\n\n\n\nIs the user new?:{}\n\n\n\n\n\n".format(is_new_user_ID))

        if is_new_user_ID:
            #self.data_sender.add_new_user_ID(self.data_dict['user_ID'], passwd)        
            self.add_new_user_ID(user_ID, passwd)

    def add_new_user_ID(self, ID, passwd):

        if not os.path.exists("/home/hgcal/FlexCableTestGUI/Data"):
            os.makedirs("/home/hgcal/FlexCableTestGUI/Data")

        if not os.path.exists("/home/hgcal/FlexCableTestGUI/Data/static"):
            os.makedirs("/home/hgcal/FlexCableTestGUI/Data/static")
            with open(self.user_path, "w") as f:
                user_data = {"users_list": ["Bryan"]}
                json.dump(user_data, f)
            f.close()
 
        if passwd == "daq5HGCAL!":
            print("Adding new user {} to user.json...".format(ID))
            with open(self.user_path, 'r') as user_json:
                user_data = json.load(user_json)
            user_json.close()

            with open(self.user_path, 'w') as user_json:
                user_data["users_list"].append(ID)
                json.dump(user_data, user_json)
            user_json.close()
            print("New user added successfully")

        else:
            print("Password incorrect. Try again")


    def get_previous_test_results(self, sn):
    
        with open(self.board_path, 'r') as board_json:
            board_data = json.load(board_json)
        board_json.close()

        return board_data[sn]["previous_results"]

    def check_if_new_board(self):
        # Send request for query
        print("testing if new board")
        self.data_dict['is_new_board'] = self.test_new_board(self.get_serial_ID())        
        print("result received:", self.data_dict['is_new_board'])
        if self.data_dict['is_new_board'] == False:
            #prev_results = self.data_sender.get_previous_test_results(self.get_serial_ID())
            prev_results = self.get_previous_test_results(self.get_serial_ID())
            for result in prev_results:
                test_id = result[0]
                pass_fail = result[1]
                if pass_fail == 0:
                    pass_fail = False
                elif pass_fail == 1:
                    pass_fail = True
                for index, test in enumerate(self.data_dict['tests_run']):
                    if test_id == test:
                        if index == 0:
                            self.data_dict['test1_pass'] = pass_fail
                            self.data_dict['test1_completed'] = pass_fail
                        elif index == 1:
                            self.data_dict['test2_pass'] = pass_fail
                            self.data_dict['test2_completed'] = pass_fail
                        elif index == 2:
                            self.data_dict['test3_pass'] = pass_fail
                            self.data_dict['test3_completed'] = pass_fail
                        elif index == 3:
                            self.data_dict['test4_pass'] = pass_fail
                            self.data_dict['test4_completed'] = pass_fail

        else:
            pass

    #################################################


    def set_user_ID(self, user_ID):

        print("\n\n\n\n\nuser_ID", user_ID)
 
        self.data_dict['user_ID'] = user_ID 
        logging.debug("DataHolder: User ID has been set.")

    ##################################################

    def set_serial_ID(self, sn):
        #self.data_sender.add_new_board(sn)
        self.add_new_board(sn)
            
        self.data_dict['current_serial_ID'] = sn
        logging.info("DataHolder: Serial Number has been set.")


    def add_new_board(self, sn):
        if not self.test_new_board(sn):
            pass
        else:
            with open(self.board_path, 'r') as f:
                board_data = json.load(f)
            f.close()

            with open(self.board_path, 'w') as board_json:
                board_data[sn] = {"previous_results": []}
                json.dump(board_data, board_json)

    
    def test_new_board(self, sn):
        logging.info("DataHolder: Checking if serial is a new board")
        #return self.data_sender.is_new_board(sn)
        return self.is_new_board(sn)

    def is_new_board(self, sn):
       
        with open(self.board_path, 'r') as board_json:
            board_data = json.load(board_json)
        board_json.close() 

        return not sn in board_data.keys()


    ##################################################

    def get_serial_ID(self):
        # TODO
        # self.data_sender.add_new_board(sn)

        return self.data_dict['current_serial_ID']

    #################################################

    # Future method to send data to the database
    def send_all_to_DB(self):
          
        person_ID = self.data_dict['user_ID']
        comments = self.data_dict['comments']
        serial_number = self.get_serial_ID()
        
         
        for i in range(len(self.data_dict['tests_run'])):
            print("Iteration:", i)
            temp = 0
            if self.data_list['test_results'][i]:
                temp = 1
            info_dict = {"serial_num":serial_number,"tester": person_ID, "test_type": self.tests_run[i], "successful": temp, "comments": comments} 
            with open("{}/PythonFiles/JSONFiles/storage.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'), "w") as outfile:
                print(info_dict)
                json.dump(info_dict, outfile)
            #self.data_sender.add_test_json("{}/PythonFiles/JSONFiles/storage.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'))
        logging.info("DataHolder: All results sent to database.")
    #################################################

    def send_to_DB(self, test_run, test_result):
        index = test_run - 1
        
        file_path_list = [
            "{}/PythonFiles/JSONFiles/Current_GenRes_JSON.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'),
            "{}/PythonFiles/JSONFiles/Current_IDRes_JSON.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'),
            "{}/PythonFiles/JSONFiles/Current_IIC_JSON.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'),
            "{}/PythonFiles/JSONFiles/Current_BERT_JSON.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI')
        ]
            

        # Converts self.test_results[index] into 1/0 instead of bool       
        temp = 0
        if test_result:
            temp = 1 


        info_dict = {"serial_num":self.get_serial_ID(),"tester": self.data_dict['user_ID'], "test_type": self.data_dict['tests_run'][index], "successful": temp, "comments": self.data_dict['comments']}
        
        with open("{}/PythonFiles/JSONFiles/storage.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'), "w") as outfile:
            print(info_dict)
            json.dump(info_dict, outfile)
        self.add_test_json("{}/PythonFiles/JSONFiles/storage.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'), file_path_list[index])
        #self.data_sender.add_test_json("{}/PythonFiles/JSONFiles/storage.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'), file_path_list[index])
        logging.info("DataHolder: Test results sent to database.")

    #################################################
  
    def add_test_json(self, in_json_path, in_data_path):
       
        with open(in_json_path, 'r') as in_json:
            data_general = json.load(in_json)
        in_json.close()

        outpath = "/home/hgcal/FlexCableTestGUI/Data/results/General/results_{}.json".format(self.get_serial_ID())

        #Get current results so we don't overwrite
        try:
            with open(outpath, 'r') as out_current:
                data_current = json.load(out_current)
            out_current.close()
        except:
            print("No results for this board yet, will be writing from scratch")
            data_current = {}


        test_type = data_general["test_type"]
        data_current['serial_num'] = data_general["serial_num"]
        data_current['tester'] = data_general['tester']
        data_current['test{}_completed'.format(test_type)] = True
        data_current['test{}_pass'.format(test_type)] = data_general['successful'] == 1
        data_current['comments'] = data_general['comments']

        # Update board results json
        with open(self.board_path, 'r') as in_board:
            board_data = json.load(in_board)
        in_board.close()
        
        board_data[str(self.get_serial_ID())]["previous_results"].append([test_type, data_general['successful']])

        with open(self.board_path, 'w') as out_board:
            json.dump(board_data, out_board)
        out_board.close()

        with open(outpath, 'w') as out_general:
            json.dump(data_current, out_general)
        out_general.close()

        test_names = ["GenRes", "", "", "BERT"] 

        current_test = test_names[int(test_type) - 1]

        outpath = "/home/hgcal/FlexCableTestGUI/Data/results/{}/results_{}_{}.json".format(current_test, self.get_serial_ID(), datetime.datetime.now())

        try:
            with open(in_data_path, 'r') as in_data:
                data_test = json.load(in_data)
            in_data.close()
        except:
            print("Issue with input data, make sure test are running correctly")
            return

        with open(outpath, 'w') as out_data:
            json.dump(data_test, out_data)
        out_data.close()
 
    def get_all_users(self):
        #users_list = self.data_sender.get_usernames() 
        users_list = self.get_usernames()
        print ("\n users_list:", users_list)
        return users_list

    def get_usernames(self):
        with open(self.user_path, 'r') as f:
            user_data = json.load(f)

        return user_data["users_list"]
        

    #################################################

    # Prints all the variable values inside data_holder
    def print(self):    
        print("data_dict: \n", self.data_dict, "\ninspection_data: \n", self.inspection_data)
    
    #################################################
    
    def update_from_json_string(self, imported_json_string):
        json_dict = json.loads(imported_json_string)

        print("Received JSON dict, printing results:")
        print(json_dict)

        test_type = json_dict["name"]

        if test_type == "RTD":
            with open("{}/PythonFiles/JSONFiles/Current_GenRes_JSON.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'), "w") as file:
                json.dump(json.loads(json_dict['data']), file)
            print("\n\n\n\n GENRES TEST \n\n\n\n")
            self.data_dict['user_ID'] = json_dict["tester"]
            self.data_dict['current_serial_ID'] = json_dict["board_sn"] 
            self.data_dict['test1_completed'] = True
            self.data_dict['test1_pass'] = json_dict["pass"]
            self.send_to_DB(1, json_dict["pass"])


        elif test_type == "ID Resistance Test":
            with open("{}/PythonFiles/JSONFiles/Current_IDRes_JSON.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'), "w") as file:
                json.dump(json_dict['data'], file)

            self.data_dict['user_ID'] = json_dict["tester"]
            self.data_dict['current_serial_ID'] = json_dict["board_sn"] 
            self.data_dict['test2_completed'] = True
            self.data_dict['test2_pass'] = json_dict["pass"]
            self.send_to_DB(2)


        elif test_type == "IIC Check":
            with open("{}/PythonFiles/JSONFiles/Current_IIC_JSON.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'), "w") as file:
                json.dump(json_dict['data'], file)

            self.data_dict['user_ID'] = json_dict["tester"]
            self.data_dict['current_serial_ID'] = json_dict["board_sn"] 
            self.data_dict['test3_completed'] = True
            self.data_dict['test3_pass'] = json_dict["pass"]
            self.send_to_DB(3)

        elif test_type == "BERT":
            with open("{}/PythonFiles/JSONFiles/Current_BERT_JSON.json".format('/home/hgcal/FlexCableTestGUI/FlexCableTestGUI'), "w") as file:
                json.dump(json_dict['data'], file)
            self.data_dict['user_ID'] = json_dict["tester"]
            self.data_dict['current_serial_ID'] = json_dict["board_sn"] 
            self.data_dict['test4_completed'] = True
            self.data_dict['test4_pass'] = json_dict["pass"]
            self.send_to_DB(4, json_dict["pass"])

        # Updates the lists
        self.data_lists['test_results'] = [self.data_dict['test1_pass'], self.data_dict['test4_pass']]
        self.data_lists['test_completion'] = [self.data_dict['test1_completed'], self.data_dict['test4_completed']]
        #self.data_lists['test_results'] = [self.data_dict['test1_pass'], self.data_dict['test2_pass'], self.data_dict['test3_pass'], self.data_dict['test4_pass']]
        #self.data_lists['test_completion'] = [self.data_dict['test1_completed'], self.data_dict['test2_completed'], self.data_dict['test3_completed'], self.data_dict['test4_completed']]

        logging.info("DataHolder: Test results have been saved")

    ################################################

    def add_inspection_to_comments(self):
        if self.inspection_data['board_chipped_bent']:
            if self.data_dict['comments'] == "_":
                self.data_dict['comments'] = ""
            self.data_dict['comments'] = self.data_dict['comments'] + " Board is chipped or bent."
        if self.inspection_data['wagon_connection_pin_bent']:
            if self.data_dict['comments'] == "_":
                self.data_dict['comments'] = ""
            self.data_dict['comments'] = self.data_dict['comments'] + " Wagon connnection pin is bent."
        if self.inspection_data['engine_connection_pin_bent']:
            if self.data_dict['comments'] == "_":
                self.data_dict['comments'] = ""
            self.data_dict['comments'] = self.data_dict['comments'] + " Engine connection pin is bent."
        if self.inspection_data['visual_scratches']: 
            if self.data_dict['comments'] == "_":
                self.data_dict['comments'] = ""
            self.data_dict['comments'] = self.data_dict['comments'] + " There are visual scratches on the board."
        if self.inspection_data['inspection_comments'] != "_": 
            if self.data_dict['comments'] == "_":
                self.data_dict['comments'] = ""
            self.data_dict['comments'] = self.data_dict['comments'] + " User comments: " + self.inspection_data['inspection_comments']
   
    ################################################

    # Keeps the login information stored
    def data_holder_new_test(self): 
        self.data_dict['current_serial_ID'] = "-1BAD"  
        self.data_dict['test1_completed'] = False
        self.data_dict['test2_completed'] = False
        self.data_dict['test3_completed'] = False
        self.data_dict['test4_completed'] = False
        self.data_dict['test1_pass'] = False     
        self.data_dict['test2_pass'] = False     
        self.data_dict['test3_pass'] = False     
        self.data_dict['test4_pass'] = False 
        self.data_dict['comments'] = "_"
        self.data_dict['is_new_board'] = False

        self.data_lists['test_results'] = [self.data_dict['test1_pass'], self.data_dict['test4_pass']]
        self.data_lists['test_completion'] = [self.data_dict['test1_completed'], self.data_dict['test4_completed']]
        #self.data_lists['test_results'] = [self.data_dict['test1_pass'], self.data_dict['test2_pass'], self.data_dict['test3_pass'], self.data_dict['test4_pass']]
        #self.data_lists['test_completion'] = [self.data_dict['test1_completed'], self.data_dict['test2_completed'], self.data_dict['test3_completed'], self.data_dict['test4_completed']]

        self.inspection_data['board_chipped_bent'] = False
        self.inspection_data['wagon_connection_pin_bent'] = False
        self.inspection_data['engine_connection_pin_bent'] = False
        self.inspection_data['visual_scratches'] = False
 
        logging.info("DataHolder: DataHolder Information has been reset for a new test.")        

    ################################################

#################################################################################
if __name__ == "__main__":
    d = DataHolder()
    d.set_serial_ID("2")   
 
    d.check_if_new_board()
    d.get_all_users()
