import random
import csv
import sys
import argparse
from email_handler import get_template, EmailHandler

class Participant:
    def __init__(self, name='no name', email='no email'):
        self.name = name
        self.email = email

    def assign_receiver(self, receiver):
        self.receiver = receiver

    def __str__(self):
        return '{}, {}'.format(self.name, self.email)

    def __eq__(self, other):
        return self.email == other.email

def get_participants(file):
    '''
    Reads a .csv-file of Participants in the following format:

    <NAME_1>,<EMAIL_1>
    <NAME_2>,<EMAIL_2>
    ...

    :param file: filename of .csv-file to read
    :returns: a list of Participants for Secret Santa
    '''
    with open(file, newline='') as participants:
        reader = csv.reader(participants)
        return [Participant(row[0], row[1]) for row in reader]

def distribute(givers):
    '''
    Provides a distribution of givers and receivers of gifts. This is done in-
    place by assigning the receiver-field of each Participant in the list.
    Ensures that a giver does not have himself/herself as a receiver.

    :param givers: a list of Participants that will be assigned receivers
    '''
    receivers = givers.copy()
    random.shuffle(receivers)
    for giver in givers:
        i = 0
        while i < len(receivers) - 1 and receivers[i] == giver:
            i += 1
        giver.assign_receiver(receivers[i])
        del receivers[i]

    if not is_valid_distribution(givers):
        for g in givers:
            g.receiver = None
        distribute(givers)

def is_valid_distribution(participants):
    '''
    Checks that a distribution of givers/receivers is valid. A valid
    distribution is defined by a list of Participants where none have their
    receiver-fields assigned to themselves.

    :param participants: a list of participants in the distribution
    :returns: True if the distribution is valid
    '''
    return all([p != p.receiver for p in participants])

def print_distribution(distribution):
    '''
    Utility function for printing a distribution.

    :param distribution: distribution to print
    '''
    print('Secret Santa 2018:')
    for participant in distribution:
        print('- {} gives to {}'.format(participant.name, participant.receiver.name))

def parse_arguments():
    parser = argparse.ArgumentParser(description='Secret Santa email distribution helper')
    parser.add_argument('--email', required=True)
    parser.add_argument('--password', required=True)
    args = parser.parse_args()
    return args.email, args.password

if __name__ == '__main__':
    email, password = parse_arguments()
    email_handler = EmailHandler(email, password)
    participants = get_participants('participants.csv')
    distribute(participants)

    for p in participants:
        print('Sending mail to {}'.format(p.email))
        message = get_template(p.name, p.email, p.receiver.name)
        email_handler.sendmail(p.email, message)

    email_handler.cleanup()
