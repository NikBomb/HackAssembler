import sys
file_path = sys.argv[1]

#initalize symbols table 
symbolsTable = {}
symbolsTable["SP"] = 0
symbolsTable["LCL"] = 1
symbolsTable["ARG"] = 2
symbolsTable["THIS"] = 3
symbolsTable["THAT"] = 4

symbolsTable["R0"] = 0
symbolsTable["R1"] = 1
symbolsTable["R2"] = 2
symbolsTable["R3"] = 3
symbolsTable["R4"] = 4
symbolsTable["R5"] = 5
symbolsTable["R6"] = 6
symbolsTable["R7"] = 7
symbolsTable["R8"] = 8
symbolsTable["R9"] = 9
symbolsTable["R10"] = 10
symbolsTable["R11"] = 11
symbolsTable["R12"] = 12
symbolsTable["R13"] = 13
symbolsTable["R14"] = 14
symbolsTable["R15"] = 15

symbolsTable["SCREEN"] = 16384
symbolsTable["KBD"] = 24576

#Computation Table
computationTable = {}
computationTable["0"] = "0101010"
computationTable["1"] = "0111111"
computationTable["-1"] = "0111010"
computationTable["D"] = "0001100"
computationTable["A"] = "0110000"
computationTable["M"] = "1110000"
computationTable["!D"]= "0001101"
computationTable["!A"]= "0110001"
computationTable["!M"]= "1110001"
computationTable["-D"]= "0001111"
computationTable["-A"]= "0110011"
computationTable["-M"]= "1110011"
computationTable["D+1"]= "0011111"
computationTable["A+1"]= "0110111"
computationTable["M+1"]= "1110111"
computationTable["D-1"]= "0001110"
computationTable["A-1"]= "0110010"
computationTable["M-1"]= "1110010"
computationTable["D+A"]= "0000010"
computationTable["D+M"]= "1000010"
computationTable["D-A"]= "0010011"
computationTable["D-M"]= "1010011"
computationTable["A-D"]= "0000111"
computationTable["M-D"]= "1000111"	
computationTable["D&A"]= "0000000"
computationTable["D&M"]= "1000000"
computationTable["D|A"]= "0010101"	
computationTable["D|M"]= "1010101"
#jump table
jumpTable = {}
jumpTable["JGT"] = "001"
jumpTable["JEQ"] = "010"
jumpTable["JGE"] = "011"
jumpTable["JLT"] = "100"
jumpTable["JNE"] = "101"
jumpTable["JLE"] = "110"
jumpTable["JMP"] = "111"

line_no =0
parsed_file = []
assembly_file = []

#first pass -> labels only and remove whitespace 
lineCounter = 0
with open(file_path, 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not (line.startswith("//") or len(line) == 0) :
            if line.startswith("("):
                symbolsTable[line.strip()[1:-1]] = lineCounter         
            else:
                lineCounter += 1
                line = line.strip()
                last_el = line.rfind("//")
                if last_el > -1:
                    parsed_file.append(line[0:last_el])
                else:
                    parsed_file.append(line)


#second pass -> write corresponding binary code
symbolsCounter = 16

for line in parsed_file:
    if line.startswith("@"):
        value = -1
        symbol = line[1:]
        if symbol.isnumeric():
            value = int(symbol)
        else:
            if symbol in symbolsTable:
                value = symbolsTable.get(symbol)
            else:
                symbolsTable[symbol] = symbolsCounter
                value =  symbolsCounter
                symbolsCounter += 1
        assembly_file.append(f'{value:016b}')
    else:
        jumpCond = line.rfind(";")
        binary_jump= "000"
        if jumpCond > -1:
            binary_jump = jumpTable.get(line[jumpCond + 1 :])
            line = line[0:jumpCond]
        assignment = line.rfind('=')
        symbolic_destination = line[0 : assignment]
        symbolic_computation = line[assignment +1 :].replace(" ", "")
        binary_destination = "000"
        if symbolic_destination.find("A") > -1:
            binary_destination = "1" + binary_destination[1] + binary_destination[2]
        if symbolic_destination.find("D") > -1:
            binary_destination = binary_destination[0] + "1" + binary_destination[2]
        if symbolic_destination.find("M") > -1:
            binary_destination = binary_destination[0:2] + "1"
        binary_computation=computationTable.get(symbolic_computation)
        assembly_file.append("111" + binary_computation + binary_destination + binary_jump)
            
# write file 
write_file = file_path.replace("asm", "hack")

with open(write_file, 'w') as f:
    for line in assembly_file:
        f.write(f"{line}\n")
