from diff import *

def getRankName(rank: str):
    match rank:
        case 'O':
            return "OK"
        case 'm':
            return "Minor problems"
        case 'M':
            return "Major problems"
        case 'U':
            return "Undecompiled"
    return '?'


def main():
    checkdir = 'Symbols'
    if len(sys.argv) == 2:
        checkdir = sys.argv[1]
    print('Checking ' + checkdir + '/')
    for subdir, dirs, files in os.walk('Symbols'):
        for file in files:
            filepath = os.path.join(subdir, file)
            syms = read_sym_file(filepath)
            newsyms = []
            for sym in syms:
                decomp_symbol = get_elf_symbol(sym[0])
                if (decomp_symbol is None):
                    newsyms.append((sym[0], sym[1], 'U', sym[3]))
                    if (sym[2] != 'U'):
                        print(sym[0] + ' ' + getRankName(sym[2]) + ' -> ' + getRankName('U'))
                else:
                    print(' ' * 80, end='\r')
                    print("Checking " + sym[0], end='\r')
                    rank = rank_symbol(sym, decomp_symbol)
                    newsyms.append((sym[0], sym[1], rank, sym[3]))
                    if (sym[2] != rank):
                        print(sym[0] + ' ' + getRankName(sym[2]) + ' -> ' + getRankName(rank))
            with open(filepath, 'w') as f:
                for sym in newsyms:
                    f.write(sym[0] + ',' + "{:08x}".format(sym[1]) + ',' + sym[3] + ',' + sym[2] + '\n')
                

if __name__ == "__main__":
    main()