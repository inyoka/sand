questions = [
    "Considerate of other people's feelings",
    "Restless, overactive, cannot stay still for long",
    "Often complains of headaches, stomach-aches or sickness",
    "Shares readily with other children (treats, toys, pencils etc)",
    "Often has a temper tantrums or hot tempers",
    "Rather solitary, tends to play alone",
    "Generally obedient, usually does what adults request",
    "Many worries, often seems worried",
    "Helpful if someone is hurt",
    "Constantly fidgeting or squirming",
    "Has at least one good friend",
    "Often fights with other children or bullies them",
    "Often unhappy, downhearted or tearful",
    "Generally liked by other children",
    "Easily distracted, concentration wanders",
    "Nervous or clingy in new situations",
    "Kind to younger children",
    "Often lies or cheats",
    "Picked on or bullied by other children",
    "Often volunteers to help others (parents, teachers, other children)",
    "Thinks things out before acting",
    "Steals from home, school or elsewhere",
    "Gets on better with adults than with other children",
    "Many fears, easily scared",
    "Sees tasks through to the end, good attention span"
]

def textLines(self):
    lines = [
        ('Birth date  :' + self.dob.get() + '\n'),
        ('Client name :' + self.name.get() + '\n'),
        ('Survey date :' + self.time + '\n'),
        ('Incomplete  :' + str(list(self.incomplete)) + '\n'),
        ('Stress score:' + str(self.stressScore) + '\n'),
        ('Emotional distress :' + str(self.fnlScore.get('emotional')) + '\n'),
        ('Behavioural difficulties :' + str(self.fnlScore.get('conduct')) + '\n'),
        ('Hyperactivity and concentration difficulties :' + str(self.fnlScore.get('hyperactivity')) + '\n'),
        ('Difficulties socialising with children :' + str(self.fnlScore.get('peer')) + '\n'),
        ('Kind and helpful behaviour :' + str(self.fnlScore.get('prosocial')) + '\n')
    ]
    return lines

def csvLines(self):
    lines = [
        (['Client ID    :']+[self.name.get()]),
        (['Birth date   :']+[self.dob.get()]),
        (['Survey date  :']+[self.time]),
        (['Incomplete   :']+[a for a in list(self.incomplete)]),
        (['PRO-SOCIAL   :']+[str(self.fnlScore['prosocial'])]),
        (['Hyperactivity:']+[str(self.fnlScore['hyperactivity'])]),
        (['Emotional    :']+[str(self.fnlScore['emotional'])]),
        (['Conduct      :']+[str(self.fnlScore['conduct'])]),
        (['Peer         :']+[str(self.fnlScore['peer'])]),
        (['Total score  :']+[self.stressScore])
    ]
    return lines


def windowLines(self):
    lines = [
        ('Client name  :'+self.name.get()+'\n'),
        ('Birth date   :'+self.dob.get()+'\n'),
        ('Survey date  :'+self.date.get()+'\n'),
        ('Incomplete   :'+', '.join(a for a in self.incomplete)+'\n'),
        ('PRO-SOCIAL   :'+str(self.fnlScore['prosocial'])+'\n'),
        ('Hyperactivity:'+str(self.fnlScore['hyperactivity'])+'\n'),
        ('Emotional    :'+str(self.fnlScore['emotional'])+'\n'),
        ('Conduct      :'+str(self.fnlScore['conduct'])+'\n'),
        ('Peer         :'+str(self.fnlScore['peer'])+'\n'),
        ('Total score  :'+str(self.stressScore))
    ]
    return lines
