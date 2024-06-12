from enum import Enum
from timeit import default_timer as timer
import config
import statistics

class hashset:
    def __init__(self):
        # TODO: create initial hash table
        self.hash_table = []

        self.verbose = config.verbose
        self.mode = config.mode
        self.hash_table_size = config.init_size

        self.colls_perInsert = []
        self.execTime_perInsert = []
        self.execTime_perFind = []
        self.num_entries = 0
        self.factor = 0.667
        self.starter = timer()
        for i in range(self.hash_table_size):
            self.hash_table.append(cell())
        
                
    # Helper functions for finding prime numbers
    def isPrime(self, n):
        i = 2
        while (i * i <= n):
            if (n % i == 0):
                return False
            i = i + 1
        return True
        
    def nextPrime(self, n):
        while (not self.isPrime(n)):
            n = n + 1
        return n

    #First hash function mode 0
    def hash1(self, input):
        h = 0
        for c in input:
            h = (h * 37 + ord(c))
            
        return h % self.hash_table_size

        # h = 0
        # for c in input:
        #     h = (h * 1_000_003 + ord(c)) % (2 ** 32)
            
        # return h % self.hash_table_size

    #Second hash function mode 4
    def hash2(self, input):
        sum = 0
        for i in range(len(input)):
            sum += ord(input[i]) * (37**(len(input)-i))        
        return sum % self.hash_table_size

        # result = 0
        # for index, character in enumerate(input):
        #     result += (index + len(input)) ** ord(character)
        #     result = result % self.hash_table_size
        # return result
    
    #Hash for Double hashing
    def dhash(self, input):
        val = 7 - (input % 7) 
        return val % self.hash_table_size

    #resizing hash_table
    def resize_set(self):
        if self.verbose > 2:
            print("Resizing the table")
            
        already_vals = []

        for i in self.hash_table:
            if i.element is not None:
                already_vals.append(i.element)

        self.hash_table = []
        self.hash_table_size *= 2

        for i in range(self.hash_table_size):
            self.hash_table.append(cell())

        for i in already_vals:
            self.insert(i)

        if self.verbose > 2:
            self.print_stats()

        return



    def insert(self, value):
        # TODO code for inserting into  hash table\
        start = timer()
        colls = 0

        load_factor = (self.num_entries+1)/self.hash_table_size

        if load_factor > self.factor:
            self.resize_set()
        
        self.num_entries += 1

        if self.mode == HashingModes.HASH_1_LINEAR_PROBING.value or self.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value or self.mode == HashingModes.HASH_1_DOUBLE_HASHING.value :
            hash_val = self.hash1(value)
        elif self.mode == HashingModes.HASH_2_LINEAR_PROBING.value or self.mode == HashingModes.HASH_2_QUADRATIC_PROBING.value or self.mode == HashingModes.HASH_2_DOUBLE_HASHING.value :
            hash_val = self.hash2(value)
        

        if self.hash_table[hash_val].element == value:
            return

        if self.hash_table[hash_val].state == state.empty:

            self.hash_table[hash_val].element = value
            self.hash_table[hash_val].state = state.in_use

        else:

            colls += 1
            i = 1
            done = False
            while not done:
                if self.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value or self.mode == HashingModes.HASH_2_QUADRATIC_PROBING.value:
                    new_index = (hash_val + i**2) % self.hash_table_size
                elif self.mode == HashingModes.HASH_1_LINEAR_PROBING.value or self.mode == HashingModes.HASH_2_LINEAR_PROBING.value:
                    new_index = (hash_val + i) % self.hash_table_size
                elif self.mode == HashingModes.HASH_1_DOUBLE_HASHING.value or self.mode == HashingModes.HASH_2_DOUBLE_HASHING.value:
                    hash_val = self.dhash(hash_val)
                    new_index = hash_val
                if self.hash_table[new_index].state == state.empty or self.hash_table[new_index].element == value:
                    self.hash_table[new_index].element = value
                    self.hash_table[new_index].state = state.in_use
                    done = True
                else:
                    i += 1
                    colls += 1
            

        end = timer()
        t = end - start
        self.execTime_perInsert.append(t)  
        self.colls_perInsert.append(colls)  
        
    def find(self, value):
        # TODO code for looking up in hash table
        start = timer()

        if self.mode == HashingModes.HASH_1_LINEAR_PROBING.value or self.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value or self.mode == HashingModes.HASH_1_DOUBLE_HASHING.value :
            hash_val = self.hash1(value)
        elif self.mode == HashingModes.HASH_2_LINEAR_PROBING.value or self.mode == HashingModes.HASH_2_QUADRATIC_PROBING.value or self.mode == HashingModes.HASH_2_DOUBLE_HASHING.value :
            hash_val = self.hash2(value)

        if self.mode != HashingModes.HASH_1_DOUBLE_HASHING.value and self.mode != HashingModes.HASH_2_DOUBLE_HASHING.value:

            for i in range(self.hash_table_size):
                if self.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value or self.mode == HashingModes.HASH_2_QUADRATIC_PROBING.value:
                    new_index = (hash_val + i**2) % self.hash_table_size
                
                elif self.mode == HashingModes.HASH_1_LINEAR_PROBING.value or self.mode == HashingModes.HASH_2_LINEAR_PROBING.value:
                    new_index = (hash_val + i) % self.hash_table_size

                if self.hash_table[new_index].state == state.empty:
                    return False
                if self.hash_table[new_index].element == value:
                    end = timer()
                    t = end - start
                    self.execTime_perFind.append(t)
                    return True

        elif self.mode == HashingModes.HASH_1_DOUBLE_HASHING.value or self.mode == HashingModes.HASH_2_DOUBLE_HASHING.value:
            
            for i in range(self.hash_table_size):
                #print("Looking")
                if self.hash_table[hash_val].state == state.empty:
                    return False
                if self.hash_table[hash_val].element == value:
                    end = timer()
                    t = end - start
                    self.execTime_perFind.append(t)
                    return True
                hash_val = self.dhash(hash_val)

        end = timer()
        t = end - start
        self.execTime_perFind.append(t)     
        #print("Placeholder")
        return False
        
    def print_set(self):
        # TODO code for printing hash table
        print("The hash table")
        for i in range(self.hash_table_size):
            print("Index: " + str(i) + " val: " + str(self.hash_table[i].element))
        
        # print("Placeholder")
        
    def print_stats(self):
        # TODO code for printing statistics
        # import csv

        ender = timer()
        t = ender - self.starter
        find_mean = str((statistics.mean(self.execTime_perFind) if self.execTime_perFind else 0) * 1000)
        insert_mean = str((statistics.mean(self.execTime_perInsert) if self.execTime_perInsert else 0) * 1000)
        num_colls = str(statistics.mean(self.colls_perInsert))

        print("Total time taken: " + str(t) + " seconds")
        print("Average insertion time: " + insert_mean + " milliseconds")
        print("Average find time: " + find_mean + " milliseconds")
        print("Average number of collisions: " + num_colls)
        print("-----------------------------------------------")
        # x = 100000
        # f = open("./data/customout/hashset/output_vary.csv", "a", newline="")
        # header = [ 'Table_Size','Insert', 'Find', 'Collisions', 'Total/s', 'Dict_Size', 'Query_Size']
        # writer = csv.writer(f)
        # # writer.writerow(header)
        
        # data = [config.init_size, float(insert_mean), float(find_mean), float(num_colls), t, x, int(0.75*x)]
        # writer.writerow(data)

        # print("Placeholder")
        
# This is a cell structure assuming Open Addressing
# It should contain and element that is the key and a state which is empty, in_use or deleted
# You will need alternative data-structures for separate chaining
class cell:
    def __init__(self, value=None):
        self.element = value
        self.state = state.empty
        
class state(Enum):
    empty = 0
    in_use = 1
    deleted = 2
        
# Hashing Modes
class HashingModes(Enum):
    HASH_1_LINEAR_PROBING=0
    HASH_1_QUADRATIC_PROBING=1
    HASH_1_DOUBLE_HASHING=2
    HASH_1_SEPARATE_CHAINING=3
    HASH_2_LINEAR_PROBING=4
    HASH_2_QUADRATIC_PROBING=5
    HASH_2_DOUBLE_HASHING=6
    HASH_2_SEPARATE_CHAINING=7
