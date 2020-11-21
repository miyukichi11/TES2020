# -*- coding: utf-8 -*-
import os

def LoadstrMatrix( filename , type = str , encoding="sjis" ):
    list = []
    for line in codecs.open( filename , "r" , encoding ):
        if line.find("//")==0:
            continue
        items = []
        for i in line.split():
            if type==str:
                items.append( i )
            else:
                items.append( type( i ) )
        list.append( items )
    return list

def LoadMatrix( filename , type = float , encoding="sjis" ):
    list = []
    for line in codecs.open( filename , "r" , encoding ):
        if line.find("//")==0:
            continue
        items = []
        for i in line.split():
            if type==str:
                items.append( i )
            else:
                items.append( type( i ) )
        list.append( items )
    return list

def LoadArray( filename , type = float , encoding="sjis" ):
    list = []
    for line in codecs.open( filename , "r" , encoding ):
        if line.find("//")==0:
            continue
        line = line.replace( "\r\n" , "" )
        line = line.replace( "\n" , "" )
        if type==str:
            list.append( line )
        else:
            list.append( type(line) )
    return list

def SaveMatrix( mat , filename , encoding="sjis" ):
    f = codecs.open( filename , "w" , encoding )
    for line in mat:
        for i in line:
            f.write( i )
            f.write( "\t" )
        f.write( "\n" )
    f.close()

def SaveintMatrix( mat , filename , encoding="sjis" ):
    f = codecs.open( filename , "w" , encoding )
    for line in mat:
        for i in line:
            f.write( int(i) )
            f.write( "\t" )
        f.write( "\n" )
    f.close()

def SaveArray( arr , filename , encoding="sjis" ):
    f = codecs.open( filename , "w" , encoding )
    for i in arr:
        f.write( i )
        f.write( "\n" )
    f.close()

def SaveintArray( arr , filename , encoding="sjis" ):
    f = codecs.open( filename , "w" , encoding )
    for i in arr:
        f.write( int(i) )
        f.write( "\n" )
    f.close()

def MakeDir( dir ):
    try:
        os.mkdir( dir )
    except:
        return False

    return True

def GetFromlistArr( data , i ):
    newData = data[6000:6001]
    for j in range(1,i):
        newData = newData + data[(j*10)+6000:(j*10)+6001]
    return newData

def GetOneFromMat( data , i ):
    newData = data[i:i+1]
    return newData

def main():
        # baseDir = "init/"
        # MakeDir( baseDir )
        # configFile = os.path.join( "MakeVariConfig.txt" )
    
        # vision = LoadstrMatrix( configFile )
    
        # print(vision)
        # mat = np.matrix(vision)
        # print(mat)
        # print(mat[0,1])
        # list = GetOneFromMat( vision , 0 )
        # print(list)
        # list = GetFromlistArr( list , 0 )
        print("test")

if __name__ == '__main__':
    main()