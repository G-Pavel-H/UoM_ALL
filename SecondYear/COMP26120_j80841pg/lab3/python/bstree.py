import config
from timeit import default_timer as timer
import statistics
# execTime_perInsert = []
# execTime_perFind = []

class bstree:


    def __init__(self):
        global execTime_perInsert
        global execTime_perFind
        global starter
        self.verbose = config.verbose

        self.value = None
        self.left = None
        self.right = None
        starter = timer()
        execTime_perInsert = []
        execTime_perFind = []

    def size(self):

        if (self.tree()):
            return 1 + (self.left.size() if self.left != None else 0) + (self.right.size() if self.right != None else 0)
    
    def height(self):

        if (self.tree()):
            return 1 + max((self.left.size() if self.left != None else 0), (self.right.size() if self.right != None else 0))

        
    def tree(self):
        # This counts as a tree if it has a field self.value
        # it should also have sub-trees self.left and self.right
        return self.value != None
        
    def insert(self, value):
        global execTime_perInsert
        start = timer()
        if (self.tree()):
            # TODO if tree is not NULL then insert into the correct sub-tree
            if value == self.value:
                return
            if value < self.value:
                if self.left == None:
                    self.left = bstree()
                    self.left.value = value
                else:
                    self.left.insert(value)
            else:
                if self.right == None:
                    self.right = bstree()
                    self.right.value = value
                else:
                    self.right.insert(value)
        else:
            # TODO otherwise create a new node containing the value
            self.value = value
        end = timer()
        t = end - start
        execTime_perInsert.append(t)
        
    def find(self, value):
        # print("to find: " + value)
        global execTime_perFind
        start = timer()
        if self.tree():
            # TODO complete the find function
            # print("the self val: " + self.value)
            
            if value == self.value:
                end = timer()
                t = end - start
                execTime_perFind.append(t)
                return True

            if value < self.value:
                if self.left != None:
                    return self.left.find(value)
                else:
                    end = timer()
                    t = end - start
                    execTime_perFind.append(t)
                    return False
            else:
                if self.right != None:
                    return self.right.find(value)
                else:
                    end = timer()
                    t = end - start
                    execTime_perFind.append(t)
                    return False
        end = timer()
        t = end - start
        execTime_perFind.append(t)
        return False
        
    # You can update this if you want
    def print_set_recursive(self, depth):
        if (self.tree()):
            for i in range(depth):
                print(" ", end='')
            print("%s" % self.value)
            if self.left != None:
                self.left.print_set_recursive(depth + 1)
            if self.right != None:
                self.right.print_set_recursive(depth + 1)
            
    # You can update this if you want
    def print_set(self):
        print("Tree:\n")
        self.print_set_recursive(0)
        
    def print_stats(self):
        # TODO update code to record and print statistic
        global execTime_perInsert
        global execTime_perFind
        global starter

        import csv

        ender = timer()
        t = ender - starter
        print("Total time: " + str(t) + " seconds")
        print("Number of Nodes: " + str(self.size()))
        print("Average Insert time: " + str(statistics.mean(execTime_perInsert)*1000) + " milliseconds")
        print("Average Find time: " + str(statistics.mean(execTime_perFind)*1000) + " milliseconds")
        print("Height of the tree: " + str(self.height()))
        
        # find_mean = (statistics.mean(execTime_perFind)) * 1000
        # insert_mean = (statistics.mean(execTime_perInsert)) * 1000
        # height = self.height()

        # x = 200000
        # f = open("./data/customout/bstree/output_752.csv", "a", newline="")
        # header = ['Insert', 'Find', 'Nodes', 'Total/s', 'Dict_Size', 'Query_Size']
        # writer = csv.writer(f)
        # # writer.writerow(header)
        
        # data = [insert_mean, find_mean, self.size(), t, x, int(0.75*x)]
        # writer.writerow(data)