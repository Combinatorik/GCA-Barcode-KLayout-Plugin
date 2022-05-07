#Script start
import pya

#Mask Name and size parameters
string="epi-etch"
scale5x=True
mirror=True
translate=True

#Function definitions
def printBlock(sequence, startPos, firstBlockBlack=False):
  black = firstBlockBlack
  for unit in sequence:
    l=unit*unitLength
    
    if black:
      top.shapes(l1).insert(pya.Box(startPos, 0, startPos+l, unitHeight))
    
    black = not black
    startPos = startPos+l
  return startPos

#Barcode hash table
barcode={' ':[1,5,1,1,1,1],
'!':[1,4,1,2,1,1],
'"':[1,4,1,1,1,2],
'#':[1,3,1,3,1,1],
'$':[1,3,1,2,1,2],
'%':[1,3,1,1,1,3],
'&':[1,3,1,1,3,1],
',':[1,3,2,1,2,1],
'(':[1,3,3,1,1,1],
')':[1,2,1,4,1,1],
'*':[1,2,1,3,1,2],
'+':[1,2,1,2,1,3],
'\'':[1,2,1,2,3,1],
'-':[1,2,1,1,1,4],
'.':[1,2,1,1,3,2],
'/':[1,2,2,2,2,1],
'0':[1,2,2,1,2,2],
'1':[1,2,3,2,1,1],
'2':[1,2,3,1,1,2],
'3':[1,1,1,5,1,1],
'4':[1,1,1,4,1,2],
'5':[1,1,1,3,1,3],
'6':[1,1,1,3,3,1],
'7':[1,1,1,2,1,4],
'8':[1,1,1,2,3,2],
'9':[1,1,1,1,1,5],
':':[1,1,1,1,3,3],
';':[1,1,1,1,5,1],
'<':[1,1,2,3,2,1],
'=':[1,1,2,2,2,2],
'>':[1,1,2,1,2,3],
'?':[1,1,2,1,4,1],
'@':[1,1,3,3,1,1],
'A':[1,1,3,2,1,2],
'B':[1,1,3,1,1,3],
'C':[1,1,3,1,3,1],
'D':[1,1,4,1,2,1],
'E':[1,1,5,1,1,1],
'F':[2,3,1,1,2,1],
'G':[2,3,2,1,1,1],
'H':[2,2,1,2,2,1],
'I':[2,2,1,1,2,2],
'J':[2,2,2,2,1,1],
'K':[2,2,2,1,1,2],
'L':[2,1,1,3,2,1],
'M':[2,1,1,2,2,2],
'N':[2,1,1,1,2,3],
'O':[2,1,1,1,4,1],
'P':[2,1,2,3,1,1],
'Q':[2,1,2,2,1,2],
'R':[2,1,2,1,1,3],
'S':[2,1,2,1,3,1],
'T':[2,1,3,1,2,1],
'U':[2,1,4,1,1,1],
'V':[3,3,1,1,1,1],
'W':[3,2,1,2,1,1],
'X':[3,2,1,1,1,2],
'Y':[3,1,1,3,1,1],
'Z':[3,1,1,2,1,2],
'[':[3,1,1,1,1,3],
'\\':[3,1,1,1,3,1],
']':[3,1,2,1,2,1],
'^':[3,1,3,1,1,1],
'_':[3,1,3,1,1,1],
'START':[4,1,2,1,1,1],
'STOP':[5,1,1,1,1,1],
'QUIET':[26.66666666666666666],
'SYNC':[1,1,1,1,1,1]}

numlist = dict(list(enumerate(barcode)))
charlist = {v: k for k, v in numlist.items()}

#script variables
unitLength = 30*1000
unitHeight=600*1000
xpos=0
textScale = 600
textOffset = -600*1000
xtranslation = 10000 * 1000
ytranslation = 11100 * 1000

if len(string) > 10:
  print("Name too long")
  exit(0)

if scale5x:
  unitLength = unitLength * 5
  unitHeight = unitHeight * 5
  textScale = textScale * 5
  textOffset = textOffset * 5
  xtranslation = xtranslation * 5
  ytranslation = ytranslation * 5

#Create new layout
layout = pya.Layout()
top = layout.create_cell("BARCODE")
l1 = layout.layer(1, 0)

#Print barcode intro section
xpos = printBlock(barcode['QUIET'], xpos, True)
xpos = printBlock(barcode['SYNC'], xpos, False)
xpos = printBlock(barcode['START'], xpos, False)

#Print name
ssum=0
string = string.upper()
for ch in string:
  try:
    xpos = printBlock(barcode[ch], xpos)
    ssum = ssum + charlist[ch]
  except:
    print("Unallowed character encountered")
    exit(0)

#Print checksum
ssum = ((ssum-1) % 64) + 1
xpos = printBlock(barcode[numlist[ssum]], xpos)

#Print termination section
xpos = printBlock(barcode['STOP'], xpos, False)
xpos = printBlock(barcode['SYNC'], xpos, True)
xpos = printBlock(barcode['QUIET'], xpos, True)

#Print name below barcode
txt_layer = pya.LayerInfo(1, 0)
param  = { "layer": txt_layer, "text": string, "mag": textScale }
txtcell = layout.create_cell("TEXT", "Basic", param)
movement = pya.Vector(xpos/4, textOffset)
trans = pya.Trans(0, False, movement)
top.insert(pya.CellInstArray.new(txtcell.cell_index(), trans))
top.flatten(True)

#Transform the overall image if necessary
if mirror:
  layout.transform(pya.DTrans.M90)
  xtranslation = xtranslation + xpos

if translate:
  xtranslation = xtranslation - xpos
  mov = pya.Trans(0, False, xtranslation, ytranslation)
  layout.transform(mov)

#Write output file
layout.write("t.gds")