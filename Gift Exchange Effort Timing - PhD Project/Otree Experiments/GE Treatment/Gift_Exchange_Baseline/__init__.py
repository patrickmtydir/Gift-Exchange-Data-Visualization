
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'Experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 13
    WORKER_ROLE = 'Worker'
    FIRM_ROLE = 'Firm'
    NUM_SUBJECTS = 10
    ENDOWMENT = 126
    COST_OF_WORKING = 26
    BID_LIST = (0, 0, 0, 0, 0, 0)
    NUM_FIRMS = 4
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    bid_number = models.IntegerField(initial=0)
    transaction_number = models.IntegerField(initial=0)
    highest_bid = models.IntegerField(initial=0)
    wage_temp = models.IntegerField()
    bid_2 = models.IntegerField(initial=0)
    bid_3 = models.IntegerField(initial=0)
    bid_4 = models.IntegerField(initial=0)
    bid_5 = models.IntegerField(initial=0)
    bid_6 = models.IntegerField(initial=0)
    group_round_number = models.IntegerField(initial=1)
def profit_calculator(group: Group):
    if group.round_number >1:
        for p in group.get_players():
            if p.type==False:
                if p.firms_offer_accepted==0:
                    p.payoff=0
                    #print("firm got profit of 0")
                if p.firms_offer_accepted==1:
                    p.payoff=(126-p.wage)*p.firm_effort_level
                    #print("wage is ",p.wage, "firm_effort_level is",p.firm_effort_level)    
            elif p.type==True:
                wage_dict={"0.1":"0","0.2":"1","0.3":"2","0.4":"4","0.5":"6","0.6":"8","0.7":"10","0.8":"12","0.9":"15","1.0":"18"}
                if p.worker_has_accepted_offer==0:
                    p.payoff=0
                if p.worker_has_accepted_offer==1:
                    #print(p.worker_effort_level)
                    wage_cost=int(wage_dict[str(p.worker_effort_level)])
                    p.payoff=p.wage_paid-26-wage_cost  
                if p.round_number == 13 and p.participant.payoff<0:
                    p.participant.payoff=cu(0)
            if p.round_number==2:
                p.round_1_payoff= int(p.payoff)
            elif p.round_number==3:
                p.round_2_payoff= int(p.payoff)
                p.round_1_payoff= int(p.in_round(p.round_number - 1).payoff)
            elif p.round_number==4:
                p.round_3_payoff= int(p.payoff)
                p.round_2_payoff= int(p.in_round(p.round_number - 1).payoff)
                p.round_1_payoff= int(p.in_round(p.round_number - 2).payoff)
            elif p.round_number==5:
                p.round_4_payoff= int(p.payoff)
                p.round_3_payoff= int(p.in_round(p.round_number - 1).payoff)
                p.round_2_payoff= int(p.in_round(p.round_number - 2).payoff)
                p.round_1_payoff= int(p.in_round(p.round_number - 3).payoff)
            elif p.round_number==6:
                p.round_5_payoff= int(p.payoff)
                p.round_4_payoff= int(p.in_round(p.round_number - 1).payoff)
                p.round_3_payoff= int(p.in_round(p.round_number - 2).payoff)
                p.round_2_payoff= int(p.in_round(p.round_number - 3).payoff)
                p.round_1_payoff= int(p.in_round(p.round_number - 4).payoff)
            elif p.round_number==7:
                p.round_6_payoff= int(p.payoff)
                p.round_5_payoff= int(p.in_round(p.round_number - 1).payoff)
                p.round_4_payoff= int(p.in_round(p.round_number - 2).payoff)
                p.round_3_payoff= int(p.in_round(p.round_number - 3).payoff)
                p.round_2_payoff= int(p.in_round(p.round_number - 4).payoff)
                p.round_1_payoff= int(p.in_round(p.round_number - 5).payoff)
            elif p.round_number==8:
                p.round_7_payoff= int(p.payoff)
                p.round_6_payoff= int(p.in_round(p.round_number - 1).payoff)
                p.round_5_payoff= int(p.in_round(p.round_number - 2).payoff)
                p.round_4_payoff= int(p.in_round(p.round_number - 3).payoff)
                p.round_3_payoff= int(p.in_round(p.round_number - 4).payoff)
                p.round_2_payoff= int(p.in_round(p.round_number - 5).payoff)
                p.round_1_payoff= int(p.in_round(p.round_number - 6).payoff)
            elif p.round_number==9:
                p.round_8_payoff= int(p.payoff)
                p.round_7_payoff= int(p.in_round(p.round_number - 1).payoff)
                p.round_6_payoff= int(p.in_round(p.round_number - 2).payoff)
                p.round_5_payoff= int(p.in_round(p.round_number - 3).payoff)
                p.round_4_payoff= int(p.in_round(p.round_number - 4).payoff)
                p.round_3_payoff= int(p.in_round(p.round_number - 5).payoff)
                p.round_2_payoff= int(p.in_round(p.round_number - 6).payoff)
                p.round_1_payoff= int(p.in_round(p.round_number - 7).payoff)
            elif p.round_number==10:
                p.round_9_payoff= int(p.payoff)
                p.round_8_payoff= int(p.in_round(p.round_number - 1).payoff)
                p.round_7_payoff= int(p.in_round(p.round_number - 2).payoff)
                p.round_6_payoff= int(p.in_round(p.round_number - 3).payoff)
                p.round_5_payoff= int(p.in_round(p.round_number - 4).payoff)
                p.round_4_payoff= int(p.in_round(p.round_number - 5).payoff)
                p.round_3_payoff= int(p.in_round(p.round_number - 6).payoff)
                p.round_2_payoff= int(p.in_round(p.round_number - 7).payoff)
                p.round_1_payoff= int(p.in_round(p.round_number - 8).payoff)
            elif p.round_number==11:
                p.round_10_payoff= int(p.payoff)
                p.round_9_payoff= int(p.in_round(p.round_number - 1).payoff)
                p.round_8_payoff= int(p.in_round(p.round_number - 2).payoff)
                p.round_7_payoff= int(p.in_round(p.round_number - 3).payoff)
                p.round_6_payoff= int(p.in_round(p.round_number - 4).payoff)
                p.round_5_payoff= int(p.in_round(p.round_number - 5).payoff)
                p.round_4_payoff= int(p.in_round(p.round_number - 6).payoff)
                p.round_3_payoff= int(p.in_round(p.round_number - 7).payoff)
                p.round_2_payoff= int(p.in_round(p.round_number - 8).payoff)
                p.round_1_payoff= int(p.in_round(p.round_number - 9).payoff)
            elif p.round_number==12:
                p.round_11_payoff= int(p.payoff)
                p.round_10_payoff= int(p.in_round(p.round_number - 1).payoff)
                p.round_9_payoff= int(p.in_round(p.round_number - 2).payoff)
                p.round_8_payoff= int(p.in_round(p.round_number - 3).payoff)
                p.round_7_payoff= int(p.in_round(p.round_number - 4).payoff)
                p.round_6_payoff= int(p.in_round(p.round_number - 5).payoff)
                p.round_5_payoff= int(p.in_round(p.round_number - 6).payoff)
                p.round_4_payoff= int(p.in_round(p.round_number - 7).payoff)
                p.round_3_payoff= int(p.in_round(p.round_number - 8).payoff)
                p.round_2_payoff= int(p.in_round(p.round_number - 9).payoff)
                p.round_1_payoff= int(p.in_round(p.round_number - 10).payoff)
            elif p.round_number==13:
                p.round_12_payoff= int(p.payoff)
                p.round_11_payoff= int(p.in_round(p.round_number - 1).payoff)
                p.round_10_payoff= int(p.in_round(p.round_number - 2).payoff)
                p.round_9_payoff= int(p.in_round(p.round_number - 3).payoff)
                p.round_8_payoff= int(p.in_round(p.round_number - 4).payoff)
                p.round_7_payoff= int(p.in_round(p.round_number - 5).payoff)
                p.round_6_payoff= int(p.in_round(p.round_number - 6).payoff)
                p.round_5_payoff= int(p.in_round(p.round_number - 7).payoff)
                p.round_4_payoff= int(p.in_round(p.round_number - 8).payoff)
                p.round_3_payoff= int(p.in_round(p.round_number - 9).payoff)
                p.round_2_payoff= int(p.in_round(p.round_number - 10).payoff)
                p.round_1_payoff= int(p.in_round(p.round_number - 11).payoff)
            p.ECU_payoff=int(p.payoff)
            p.ECU_payoff_total=int(p.participant.payoff)
            p.USD_payoff=p.ECU_payoff_total/25
            p.USD_payoff_with_showup=float(p.participant.payoff_plus_participation_fee())
            #print("player profit is", p.payoff)
def role_assign_group(group: Group):
    import time 
    group.group_round_number=group.round_number-1
    for p in group.get_players():
        #print("role assigned for",p.id_in_group)
        if p.id_in_group <=C.NUM_FIRMS: #change later back to <=4
            p.type=0
        else:
            p.type=1
            p.effort_start_time=time.time() 
class Player(BasePlayer):
    IRB = models.BooleanField(initial=False)
    type = models.BooleanField(choices=[[True, 'Worker'], [False, 'Firm']])
    Q1 = models.BooleanField(choices=[[True, 'True'], [False, 'False']], label='Question 1: True or False? Workers make bids on their wages', widget=widgets.RadioSelect)
    Q2 = models.IntegerField(label='Question 2: If a worker provides an effort of 0.6, then what is the cost of effort?')
    Q3 = models.IntegerField(label='Question 3: If a worker receives a wage of 56 and provides an effort of 0.7, then what is their profit for the period?')
    Q4 = models.IntegerField(label="Question 4: If a firm hires a worker for 46 ECUs and the worker provides an effort of 0.5, then what is the firm's profit?")
    money_after_wage = models.IntegerField()
    firms_offer_accepted = models.BooleanField(initial=False)
    worker_has_accepted_offer = models.BooleanField(initial=False)
    wage_paid = models.IntegerField(initial=0)
    transaction_number = models.IntegerField(initial=0)
    wage = models.IntegerField(initial=-1)
    firms_worker_id = models.IntegerField(initial=0)
    bid_number = models.IntegerField(initial=-185)
    number_of_offers_in_round = models.IntegerField(initial=0)
    previous_wage = models.IntegerField()
    previous_bid_number = models.IntegerField()
    worker_selected_effort = models.BooleanField(initial=False)
    worker_effort_level = models.FloatField(initial=0.1)
    firm_effort_level = models.FloatField(initial=0)
    effort_cost = models.IntegerField(initial=0)
    ECU_payoff = models.IntegerField()
    ECU_payoff_total = models.IntegerField(initial=0)
    accepted_highest_offer = models.BooleanField(initial=False)
    bid_placement_of_accepted_offer = models.IntegerField()
    time_offered = models.FloatField()
    time_bought = models.FloatField()
    time_to_bought = models.FloatField()
    time_to_effort = models.FloatField()
    effort_start_time = models.FloatField()
    auction_start_time =models.FloatField()
    Instructions_Page_Number = models.IntegerField(initial=1, max=10, min=1)
    wrong_string = models.StringField(initial='')
    previous_answers = models.StringField(initial='')
    worker_has_selected_effort = models.BooleanField(initial=False)
    USD_payoff = models.FloatField(initial=0)
    USD_payoff_with_showup = models.FloatField()
    First_Name = models.StringField(initial='', label='First Name:')
    Last_Name = models.StringField(initial='', label='Last Name:')
    has_given_info = models.BooleanField(initial=False)
    round_1_payoff = models.IntegerField(initial=0)
    round_2_payoff = models.IntegerField(initial=0)
    round_3_payoff = models.IntegerField(initial=0)
    round_4_payoff = models.IntegerField(initial=0)
    round_5_payoff = models.IntegerField(initial=0)
    round_6_payoff = models.IntegerField(initial=0)
    round_7_payoff = models.IntegerField(initial=0)
    round_8_payoff = models.IntegerField(initial=0)
    round_9_payoff = models.IntegerField(initial=0)
    round_10_payoff = models.IntegerField(initial=0)
    round_11_payoff = models.IntegerField(initial=0)
    round_12_payoff = models.IntegerField(initial=0)
def live_method(player: Player, data):
    group = player.group
    import time
    
    if data["information_type"]=="offer" and data["wage"]>group.highest_bid and data["wage"] % 5==0 and data["wage"]<=126 and data["wage"]>=26 and data['wage'] % 1 ==0 and player.firms_offer_accepted==False: 
        player.previous_bid_number=player.bid_number
        if player.wage==group.highest_bid: #Have to make sure all these if statements work and make sense!!
            group.highest_bid=data["wage"]
        elif player.wage==group.bid_2:
            group.bid_2=group.highest_bid    
            group.highest_bid=data["wage"]
        elif player.wage==group.bid_3:
            group.bid_3=group.bid_2
            group.bid_2=group.highest_bid    
            group.highest_bid=data["wage"]
        elif player.wage==group.bid_4:
            group.bid_4=group.bid_3
            group.bid_3=group.bid_2
            group.bid_2=group.highest_bid    
            group.highest_bid=data["wage"]
        elif player.wage==group.bid_5:
            group.bid_5=group.bid_4
            group.bid_4=group.bid_3
            group.bid_3=group.bid_2
            group.bid_2=group.highest_bid    
            group.highest_bid=data["wage"]
        elif player.wage==group.bid_6:
            group.bid_6=group.bid_5
            group.bid_5=group.bid_4
            group.bid_4=group.bid_3
            group.bid_3=group.bid_2
            group.bid_2=group.highest_bid    
            group.highest_bid=data["wage"]
        elif player.wage != group.highest_bid and player.wage != group.bid_2 and player.wage != group.bid_3 and player.wage != group.bid_4 and player.wage != group.bid_5 and player.wage != group.bid_6:
            group.bid_6=group.bid_5
            group.bid_5=group.bid_4
            group.bid_4=group.bid_3
            group.bid_3=group.bid_2
            group.bid_2=group.highest_bid
            group.highest_bid=data["wage"]
        #print("Bid list is", group.highest_bid, group.bid_2, group.bid_3, group.bid_4, group.bid_5, group.bid_6)
        group.bid_number=group.bid_number+1
        player.bid_number=group.bid_number
        player.wage=data["wage"]
        #print ("Proper wage offer recieved on python",data)
        player.time_offered=time.time()-player.auction_start_time
        #print("time_offered is", player.time_offered)
        player.number_of_offers_in_round=player.number_of_offers_in_round+1
        if player.type==0 and player.wage==data["wage"] and player.id_in_group == data["id_in_group"]:
            #print(Bid.filter())
            Bid.create(player=player , round_number=player.round_number, firm_ID=player.id_in_group, wage=player.wage, bid_number=player.bid_number, time_offered=player.time_offered, number_of_offers=player.number_of_offers_in_round)
            #print(Bid.filter())
        #print(Bids.filter(player=player))
        return {0: dict(information_type="offer", wage=data["wage"], bid_number=player.bid_number, firm_id=player.id_in_group, previous_bid_number=player.previous_bid_number)}
    if data["information_type"]=="offer": # and data["id_in_group"]==player.id_in_group
        #print ("Improper wage offer recieved on python",data)
        error_dict=dict(information_type="error_message", not_int="False", too_high_bid="False",low_bid="False",not_multiple_of_5="False", id_in_group=player.id_in_group)
        if data["wage"] % 1 !=0:
            error_dict["not_int"]="True"
        if data["wage"]>126:
            error_dict["too_high_bid"]="True"
        if data["wage"]<=group.highest_bid or data["wage"]<26:
            error_dict["low_bid"]="True"
        if data["wage"] % 5 !=0:
            error_dict["not_multiple_of_5"]="True"
        #print ("Bid_error recieved",data)
        return {player.id_in_group: error_dict}    #data["id_in_group"]
    
    if data["information_type"]=="accept":  # and data["offer_number"]>0
        #print ("Acceptance recieved on python",data)
        temp_group=player.get_others_in_group()
        firm_identified=False
        for p in temp_group:
            #print("looped over player number ",p.id_in_group)
            if p.bid_number==data["offer_number"]:
                firm=p
                firm_identified=True
                #print("firm is:",firm)
        #if data["offer_number"]==player.bid_number:
        if firm_identified==True:
            if player.worker_has_accepted_offer==True:
                print("player.worker_has_accepted_offer is True but he submitted an accept, this should not occur",player.worker_has_accepted_offer)
            if firm.firms_offer_accepted==False and player.worker_has_accepted_offer== False:
                firm.firms_offer_accepted=True
                player.worker_has_accepted_offer=True
                #firm.firms_worker_id=player.id_in_group
                group.transaction_number=group.transaction_number+1
                firm.transaction_number=group.transaction_number
                player.transaction_number=group.transaction_number
                player.wage_paid=firm.wage
                firm.firms_worker_id=player.id_in_group
                if firm.wage==group.highest_bid:
                    player.accepted_highest_offer=True
                    player.bid_placement_of_accepted_offer=1
                    group.highest_bid=group.bid_2
                    group.bid_2=group.bid_3
                    group.bid_3=group.bid_4
                    group.bid_4=group.bid_5
                    group.bid_5=group.bid_6
                    group.bid_6=0
                elif firm.wage==group.bid_2:
                    player.bid_placement_of_accepted_offer=2
                    group.bid_2=group.bid_3
                    group.bid_3=group.bid_4
                    group.bid_4=group.bid_5
                    group.bid_5=group.bid_6
                    group.bid_6=0
                elif firm.wage==group.bid_3:
                    player.bid_placement_of_accepted_offer=3
                    group.bid_3=group.bid_4
                    group.bid_4=group.bid_5
                    group.bid_5=group.bid_6
                    group.bid_6=0
                elif firm.wage==group.bid_4:
                    player.bid_placement_of_accepted_offer=4
                    group.bid_4=group.bid_5
                    group.bid_5=group.bid_6
                    group.bid_6=0
                elif firm.wage==group.bid_5:
                    player.bid_placement_of_accepted_offer=5
                    group.bid_5=group.bid_6
                    group.bid_6=0
                elif firm.wage==group.bid_6:
                    player.bid_placement_of_accepted_offer=6
                    group.bid_6=0
                #print("worker accepted the",player.bid_placement_of_accepted_offer," highest offer")
                firm.time_bought=time.time()-player.auction_start_time
                firm.time_to_bought=firm.time_bought-firm.time_offered           
                #print("time_bought is", firm.time_bought,"and time_to_bought is ",firm.time_to_bought)
                firm.firm_effort_level=player.worker_effort_level
                wage_dict={"0.1":"0","0.2":"1","0.3":"2","0.4":"4","0.5":"6","0.6":"8","0.7":"10","0.8":"12","0.9":"15","1.0":"18"}
                wage_cost=int(wage_dict[str(player.worker_effort_level)])
                worker_surplus=player.wage_paid-26-wage_cost
                firm_surplus=(126-firm.wage)*firm.firm_effort_level
                if player.round_number>1:
                    Transaction.create(player=player, round_number=player.round_number, worker_ID=player.id_in_group, firm_ID=firm.id_in_group, wage=firm.wage, effort=player.worker_effort_level, transaction_number=firm.transaction_number, bid_number=firm.bid_number, offer_placement=player.bid_placement_of_accepted_offer, highest_offer_accepted_boolean=player.accepted_highest_offer, worker_surplus=worker_surplus,firm_surplus=firm_surplus, time_offered=firm.time_offered, time_accepted=firm.time_bought, time_to_accept=firm.time_to_bought, number_of_offers=firm.number_of_offers_in_round, time_to_effort=player.time_to_effort)

                return {0:dict(information_type="accept", offer_number=firm.bid_number,wage=firm.wage, transaction_number=firm.transaction_number,firm_id=firm.id_in_group,worker_id=player.id_in_group)}
            if firm.firms_offer_accepted==True: 
                #print("Firm has already had offer accepted", data)
                return {player.id_in_group: dict(information_type="firm_already_hired_error")} 
        if firm_identified==False:
            return {player.id_in_group: dict(information_type="invalid_transaction_number")} 
    
def live_effort(player: Player, data):
    import time
    group = player.group
    if data["information_type"]=="effort":
        if data["id_in_group"]==player.id_in_group and player.worker_selected_effort==False:
            player.time_to_effort=time.time()-player.effort_start_time
            player.worker_selected_effort=True
            player.worker_effort_level=data["effort"]
            wage_dict={"0.1":"0","0.2":"1","0.3":"2","0.4":"4","0.5":"6","0.6":"8","0.7":"10","0.8":"12","0.9":"15","1":"18"}
            player.effort_cost=int(wage_dict[str(player.worker_effort_level)])+26
        elif data["id_in_group"]==player.id_in_group and player.worker_selected_effort==True:
            print("worker has already selected effort")                
    
def live_IRB(player: Player, data):
    group = player.group
    if data["information_type"]=="IRB":
        #if player.id_in_group <=C.NUM_FIRMS: #change later back to <=4
           # player.type=0
        #else:
            #player.type=1
        player.IRB=True
        #print("Player number ",player.id_in_group, " has read the information sheet.")
def live_payment(player: Player, data):
    if data["information_type"]=="answers":
        print("live_payment executing",data)
        player.has_given_info=True
        player.First_Name=data['FN']
        player.Last_Name=data["LN"]
        player.Venmo_Account=data["VA"]
        player.FSU_Email=data["FE"]
        #print(player.First_Name,player.Last_Name,player.FSU_Email,player.Venmo_Account)
def custom_export(players):
    #Header row
    yield ["round_number","firm_id","wage","bid_number","time_offered","number_of_offers"]
    bids=Bid.filter()
    for bid in bids:
        player=bid.player
        yield [bid.round_number, bid.firm_ID, bid.wage, bid.bid_number, bid.time_offered, bid.number_of_offers]
#    yield ["This is the break between tables"]
    yield ["round_number","firm_id","wage","bid_number","time_offered","number_of_offers", "worker_id", "effort", "transaction_number", "offer_placement", "highest_offer_accepted_boolean", "worker_surplus", "firm_surplus", "time_accepted", "time_to_accept", "time_to_effort"]
    transactions=Transaction.filter()
    for transaction in transactions:
        player=transaction.player
        yield [transaction.round_number, transaction.firm_ID, transaction.wage, transaction.bid_number, transaction.time_offered, transaction.number_of_offers, transaction.worker_ID, transaction.effort, transaction.transaction_number, transaction.offer_placement, transaction.highest_offer_accepted_boolean, transaction.worker_surplus, transaction.firm_surplus, transaction.time_accepted, transaction.time_to_accept, transaction.time_to_effort]    
        #(group=player.group, player=player, round_number=player.round_number, worker_ID=player.id_in_group, firm_ID=firm.id_in_group, wage=firm.wage, effort=player.worker_effort_level, transaction_number=player.transaction_number, bid_number=firm.bid_number, offer_placement=player.bid_placement_of_accepted_offer, highest_offer_accepted_boolean=player.accepted_highest_offer, worker_surplus=worker_surplus,firm_surplus=firm_surplus, time_offered=firm.time_offered, time_accepted=firm.time_bought, time_to_accept=firm.time_to_bought, number_of_offers=firm.number_of_offers_in_round)


class Bid(ExtraModel):
    group=models.Link(Group)
    player=models.Link(Player)
    round_number=models.IntegerField()
    firm_ID=models.IntegerField()
    wage=models.IntegerField()
    bid_number=models.IntegerField()
    time_offered=models.FloatField()
    number_of_offers=models.IntegerField()

class Transaction(ExtraModel):
    group=models.Link(Group)
    player=models.Link(Player)
    round_number=models.IntegerField()
    worker_ID=models.IntegerField()
    firm_ID=models.IntegerField()
    wage=models.IntegerField()
    effort=models.FloatField()
    transaction_number=models.IntegerField()
    bid_number=models.IntegerField()
    offer_placement=models.IntegerField()
    highest_offer_accepted_boolean=models.BooleanField()
    worker_surplus=models.FloatField()
    firm_surplus=models.FloatField()
    time_offered=models.FloatField()
    time_accepted=models.FloatField()
    time_to_accept=models.FloatField()
    time_to_effort=models.FloatField()
    number_of_offers=models.IntegerField()


class IRB_Info(Page):
    form_model = 'player'
    live_method = 'live_IRB'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    @staticmethod
    def js_vars(player: Player):
        group = player.group
        return dict(
        id_in_group=player.id_in_group)
class Instructions_Quiz(Page):
    form_model = 'player'
    form_fields = ['Q1', 'Q2', 'Q3', 'Q4']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict()
    @staticmethod
    def error_message(player: Player, values):
        error_string="Please check your answers for the following question(s): "
        hint_string=""
        error_occured=False
        if values["Q1"] !=False :
            error_string=error_string+"1 "
            error_occured=True
            hint_string=hint_string+"Hint 1: Firms make bids on wages, "
        if values["Q2"] != 8:
            error_string=error_string+"2 "
            error_occured=True
            hint_string=hint_string+"Hint 2: Look at the cost of effort corresponding to an effort of 0.6 in the Cost of Effort table, "
        if values["Q3"] != 20:
            error_string=error_string+"3 "
            error_occured=True
            hint_string=hint_string+"Hint 3: Worker profit=wage-Cost of Effort-26=56-10-26, "
        if values["Q4"] != 40:
            error_string=error_string+"4 "
            error_occured=True
            hint_string=hint_string+"Hint 4: Firm Profit=(126-Wage)xEffort Level = (126-46)x0.5"
        if error_occured ==True:
            return error_string+hint_string
class Role_assign_waitpage(WaitPage):
    after_all_players_arrive = role_assign_group
class Instructions_Quiz_Pause(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
class Stage_2_Pause(Page):
    form_model = 'player'
    timeout_seconds = 5
    timer_text = "Time before Stage 1:"
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import time
        player.auction_start_time=time.time() 
class Stage_2(Page):
    form_model = 'player'
    timeout_seconds = 60
    timer_text = 'Time left in Stage 1:'
    live_method = 'live_method'
    @staticmethod
    def js_vars(player: Player):
        group = player.group
        return dict(
            id_in_group=player.id_in_group,
            type=player.type,
            transaction_number=player.transaction_number,
            bid_number=player.bid_number,
            group_highest_bid=group.highest_bid,
            worker_has_accepted_offer=player.worker_has_accepted_offer
        )
class Instructions_Stage_2_Pause(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1  
class Effort_Selection(Page):
    form_model = 'player'
    live_method = 'live_effort'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number >1 and player.type==1
    @staticmethod
    def js_vars(player: Player):
        group = player.group
        return dict(
            id_in_group=player.id_in_group,
            type=player.type,
            transaction_number=player.transaction_number,
            bid_number=player.bid_number,
            group_highest_bid=group.highest_bid,
            worker_has_accepted_offer=player.worker_has_accepted_offer)
class Stage_2_Waitpage(WaitPage):
    after_all_players_arrive = profit_calculator
class Effort_Waitpage(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number >1
class Period_Payoffs(Page):
    form_model = 'player'
    timeout_seconds = 20
    timer_text = 'Time Before Next Round'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number >1
class Payment_Page(Page):
    form_model = 'player'
    form_fields = ['First_Name', 'Last_Name']
    live_method = 'live_payment'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 13
class Experiment_End(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 13
page_sequence = [IRB_Info, Instructions_Quiz, Role_assign_waitpage, Instructions_Quiz_Pause, Effort_Selection, Effort_Waitpage, Stage_2_Pause, Stage_2, Stage_2_Waitpage, Instructions_Stage_2_Pause, Period_Payoffs, Payment_Page, Experiment_End]