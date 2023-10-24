import argparse
import sys
import msat_runner
import wcnf

class Auction:

    def __init__(self, solver=None, flag = False):
        self.flag = flag #--no-min-win-bids activated (false by default)
        self.formula = wcnf.WCNFFormula()
        self.solver = solver
        self.goods = set() #Set of tuples (good, bid)
        self.auctions = [] #List of bids (agent, good1, good2, ..., goodn, price)
        self.auctioneers = [] #List of auctioneers

    def read_file(self, file):
        if file:
            with open(file, 'r', encoding="utf8") as stream:
                return self.parse_input_stream(stream)
        else:
            raise FileNotFoundError

    def parse_input_stream(self, stream):
        reader = (l for l in (ll.strip() for ll in stream) if l)
        for line in reader:
            l = line.split()
            if l[0] == 'a':#add the auctioneers to the set
                for auctioneer in range(1, len(l)):
                    self.auctioneers.append(l[auctioneer])
            if l[0] != 'g' and l[0] != 'a': #Other lines are bids
                self.auctions.append(l)
                self.manage_auction(l)

        self.manage_incompatibilities(self.goods)
        if self.flag:
            solution = self.solver.solve(self.formula)
        else:
            solution = self.check_all_auctioneers_win(self.formula)

        return solution

    def check_all_auctioneers_win(self, formula):
        #Check if all auctioneers win at least one of his bids
        for auctioneer in self.auctioneers:
            auctions_of_auctioneer = []
            #add a clause for the set of bids of every auctioneer
            for auction in self.auctions:
                if auctioneer == auction[0]:
                    auctions_of_auctioneer.append(self.auctions.index(auction)+1)
            formula.add_clause(auctions_of_auctioneer, wcnf.TOP_WEIGHT)

        solution = self.solver.solve(formula)
        return solution
    def manage_auction(self, bid):
        #Every bid has a unique id
        weight = int(bid[-1])
        actual_auction = self.formula.new_var()
        self.formula.add_clause([actual_auction], weight) #SOFT CLAUSE: page 29 PowerPoint
        for good in bid[1:len(bid)-1]:
                self.goods.add((good, actual_auction)) #Add all the goods to the set

    def manage_incompatibilities(self, goods):
        for good in goods:
            for good2 in goods:
                if good[0] == good2[0] and good[1] != good2[1] and good[1] < good2[1] and [-good[1], -good2[1]] not in self.formula.hard: #The same good and different bids bid1 < bid2 used to avoid duplicates, same with not in self.formula.hard
                    self.formula.add_clause([-good[1], -good2[1]], wcnf.TOP_WEIGHT)

    def print_solution(self, solution):
        opt, bids = solution
        winning_bids = []
        benefit = self.formula.sum_soft_weights() - opt #benefit = sum of all bids - opt
        for bid in bids:
            if bid > 0:
                winning_bids.append(bid) #add the winning bids to the list

        print("Benefit: " + str(benefit))

        for bid in winning_bids:
            to_print = (self.auctions[bid-1])
            agent = to_print[0]
            goods = to_print[1:len(to_print)-1]
            price = to_print[-1]
            print(agent + ": " + ",".join(goods) + " (Price " + price + ")")

        if(benefit > self.formula.sum_soft_weights()): #Check if the benefit is greater than the sum of all bids
            print("Invalid solution")
        else:
            print("Valid solution")

def main(argv=None):
    """
    Creates an object that represents the problem,
    then solve it and print its solution.
    Also, if the "--validate" option has been called, validate the answer
    """
    args = parse_args(argv)
    solver = msat_runner.MaxSATRunner(args.solver)
    flag = args.no_min_win_bids
    auct_problem = Auction(solver, flag)
    solution = auct_problem.read_file(args.input_file)
    auct_problem.print_solution(solution)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('solver', help='The path to MAXSAT solver to use')
    parser.add_argument('input_file', help='The path to the input file.')
    parser.add_argument('--no-min-win-bids', action='store_true', help='Minimum winning bids constraints disabled.')

    return parser.parse_args(args=argv)

if __name__ == '__main__':
    sys.exit(main())
