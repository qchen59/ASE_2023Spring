**Report**


**Interview 1 & attributes**

We chose cars as our domain. Our first interviewee came up with cars of different makes. That includes compact cars (gas and electric), trucks, SUVs, as well as sports cars. The attributes chosen cover high-level differences in cars such as looks, price, and engine sounds. 


The clusters, in terms of examples, put the cars that are compact together, luxury together, and sporty together. The Ford F-150 stands alone.


Running clustering on cols gave us some great ideas for synonyms. Such as QuietEngine:LoudEngine is synonymous with FunctionBase:EnjoymentBased which makes sense, enjoyment-based cars usually have loud, powerful engines, and this is why people like them. SmallExterior:LargeExterior and MinimalDriverConsole:ClutteredDriverConsole are also somehow related because larger cars have larger interior space for the driver console.


From the repPlace results, we can see that the compact cars are close to each other. Compact cars usually have a similar exterior size and price, and most are function based.


**Interview 2**

Our second interviewee provided similar high-level attributes such as price, usage, driver console layout, and shape, which gave us good examples to compare with interview 1.


The prototype results are largely different from interview 1, except the Ford F-150 stand-alone and Porsche 911 and Lamborghini Urus are together. This shows that even with similar attributes, different people have different views, which leads to various results.


The synonyms also give us some great ideas. Such as Affordable:Expensive and LowAwarenessTechnology:HighAwarenessTechnology. High awareness technology cars definitely are more expensive. ShortDistanceDriveCar:LongDistanceDriveCar and ComplexButtonLayout:SimpleButtonLayout is a tricky one. We may want more examples to ensure this one, but it also makes sense in some circumstances.


The repPlace is more spread out. But some examples stay close, such as the Ford Mustang and Ford F-150, probably because Ford has a similar style of shape and button layout design on both of them.


**Interview 3**

Our third interviewee gave us some very interesting detailed attributes about the driving experience of each car, such as handling, visibility, and seat. They are great information that shows how those different attributes work.


The Porsche 911 and Lamborghini Urus still stay together this time. AudiA8 and Polestars are together as interview 2. FordMustang stands alone by itself.


The synonyms results are also interesting. SeatNotComfortable:SeatVeryComfortable and InfotainmentHardToUse:InfotainmentEasyToUse are synonyms. This makes sense since they both touch on the user experience. BadHandling:GoodHandling and RideVeryRough:RideVerySmooth make sense.


For repPlace, Mustang stands away from others(maybe there is no other muscle car in our example lists)


**Overview**


Those interview results provided great information about people’s perspectives in evaluating cars and how cars/attributes are related to each other based on their scores. The clustering results gave us some innovative opinions. Interestingly, in all three results, Lamborghini Urus and Porsche 911, those two extremely luxurious things stayed together as prototypes even the interview 3 didn’t include price as an attribute. Another thing is that we can see how those electric cars are being identified or clustered. There is no attribute associated with electric or gas cars because it is more like a binary attribute, but they have some similarities.





## Interview 1:
```

local _ = " "

return {

domain="Cars",

cols={   {'SmallExterior', 1, 4, 1, 2, 1, 5, 2, 3, 4, 3, 'LargeExterior'},

         {'CurvedExterior', 1, 4, 1, 2, 3, 5, 3, 5, 3, 4, 'AngledExterior'},

         {'Affordable', 3, 2, 5, 4, 1, 3, 3, 4, 5, 2, 'Expensive'},

         {'MinimalDriverConsole' , 1, 3, 3, 3, 2, 4, 3, 2, 3, 4, 'ClutteredDriverConsole'},

         {'FunctionBased', 4, 2, 5, 4, 1, 1, 3, 3, 5, 5, 'EnjoymentBased'},

         {'QuietEngine', 1, 2, 4, 3, 2, 4, 3, 1, 5, 5, 'LoudEngine'}},

rows={                      { _, _, _, _, _, _, _, _, _, 'FordMustang'},

                           { _, _, _, _, _, _, _, _, 'LamborghiniUrus'},

                           { _, _, _, _, _, _, _, 'Polestar2'},

                           { _, _, _, _, _, _, 'InfinityQ60'},

                           { _, _, _, _, _,  'FordF150'},

                           { _, _, _, _,  'ToyotaCamry'},

                           { _, _, _,  'AudiA8'},

                           { _, _,  'Porsche911'},

                           { _, 'HondaCRV'},

                           {'TeslaModel3'}}

}
```

```
73
|..48
|..|..45
|..|..|..ToyotaCamry
|..|..|..TeslaModel3
|..|..35
|..|..|..Polestar2
|..|..|..29
|..|..|..|..InfinityQ60
|..|..|..|..HondaCRV
|..54
|..|..38
|..|..|..LamborghiniUrus
|..|..|..Porsche911
|..|..57
|..|..|..FordF150
|..|..|..41
|..|..|..|..AudiA8
|..|..|..|..FordMustang


79
|..51
|..|..Affordable:Expensive
|..|..49
|..|..|..QuietEngine:LoudEngine
|..|..|..FunctionBased:EnjoymentBased
|..51
|..|..CurvedExterior:AngledExterior
|..|..50
|..|..|..SmallExterior:LargeExterior
|..|..|..MinimalDriverConsole:ClutteredDriverConsole

A TeslaModel3
B HondaCRV
C Porsche911
D AudiA8
E ToyotaCamry
F FordF150
G InfinityQ60
H Polestar2
I LamborghiniUrus
J FordMustang

[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', 'E', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'I', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', 'G', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'D', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'J', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', 'A', ' ', 'H', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']


```



## Interview 2:
```

local _ = " "

return {

domain="Cars",

cols={   {'Affordable', 3, 2, 5, 4, 1, 2, 3, 4, 5, 2, 'Expensive'},

         {'ShortDistanceDriveCar', 4, 5, 1, 3, 5, 4, 3, 2, 2, 2, 'LongDistanceDriveCar'},

         {'IndividualOriented', 4, 5, 1, 3, 5, 1, 4, 4, 5, 3, 'FamilyOriented'},

         {'ComplexButtonLayout', 5, 3, 2, 3, 1, 2, 2, 4, 2, 3, 'SimpleButtonLayout'},

         {'LowAwarenessTechnology', 5, 3, 4, 3, 2, 2, 4, 5, 4, 2, 'HighAwarenessTechnology'},

         {'SmoothShape', 1, 4, 1, 2, 3, 5, 2, 4, 2, 5, 'AggressiveShape'}},

rows={                      { _, _, _, _, _, _, _, _, _, 'FordMustang'},

                           { _, _, _, _, _, _, _, _, 'LamborghiniUrus'},

                           { _, _, _, _, _, _, _, 'Polestar2'},

                           { _, _, _, _, _, _, 'InfinityQ60'},

                           { _, _, _, _, _,  'FordF150'},

                           { _, _, _, _,  'ToyotaCamry'},

                           { _, _, _,  'AudiA8'},

                           { _, _,  'Porsche911'},

                           { _, 'HondaCRV'},

                           {'TeslaModel3'}}

}
```

```
79
|..49
|..|..28
|..|..|..ToyotaCamry
|..|..|..HondaCRV
|..|..53
|..|..|..FordF150
|..|..|..46
|..|..|..|..InfinityQ60
|..|..|..|..FordMustang
|..58
|..|..43
|..|..|..Porsche911
|..|..|..LamborghiniUrus
|..|..40
|..|..|..TeslaModel3
|..|..|..38
|..|..|..|..AudiA8
|..|..|..|..Polestar2


68
|..61
|..|..IndividualOriented:FamilyOriented
|..|..35
|..|..|..Affordable:Expensive
|..|..|..LowAwarenessTechnology:HighAwarenessTechnology
|..54
|..|..SmoothShape:AggressiveShape
|..|..51
|..|..|..ShortDistanceDriveCar:LongDistanceDriveCar
|..|..|..ComplexButtonLayout:SimpleButtonLayout

A TeslaModel3
B HondaCRV
C Porsche911
D AudiA8
E ToyotaCamry
F FordF150
G InfinityQ60
H Polestar2
I LamborghiniUrus
J FordMustang

[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', 'E', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'C', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'G', ' ', 'D', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'I', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', 'J', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', 'F', ' ', ' ', ' ', ' ', 'H', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'A', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']


```



## Interview3:
```

local _ = " "

return {

domain="Cars",

cols={   {'SeatNotComfortable', 4, 3, 5, 5, 3, 3, 4, 5, 5, 2, 'SeatVeryComfortable'},

         {'BadHandling', 2, 2, 5, 4, 2, 1, 3, 3, 5, 2, 'GoodHandling'},

         {'BadVisibility', 5, 4, 3, 2, 3, 2, 4, 4, 4, 1, 'GoodVisibility'},

         {'InfotainmentHardToUse', 2, 3, 4, 3, 5, 4, 3, 3, 3, 1, 'InfotainmentEasyToUse'},

         {'RideVeryRough', 4, 3, 4, 5, 3, 1, 4, 5, 5, 1, 'RideVerySmooth'},

         {'SimpleMaintenance', 2, 5, 3, 3, 5, 4, 5, 1, 2, 4, 'ComplexMaintenance'}},

rows={                      { _, _, _, _, _, _, _, _, _, 'FordMustang'},

                           { _, _, _, _, _, _, _, _, 'LamborghiniUrus'},

                           { _, _, _, _, _, _, _, 'Polestar2'},

                           { _, _, _, _, _, _, 'InfinityQ60'},

                           { _, _, _, _, _,  'FordF150'},

                           { _, _, _, _,  'ToyotaCamry'},

                           { _, _, _,  'AudiA8'},

                           { _, _,  'Porsche911'},

                           { _, 'HondaCRV'},

                           {'TeslaModel3'}}

}
```

```
60
|..53
|..|..30
|..|..|..ToyotaCamry
|..|..|..InfinityQ60
|..|..45
|..|..|..FordMustang
|..|..|..34
|..|..|..|..HondaCRV
|..|..|..|..FordF150
|..38
|..|..20
|..|..|..LamborghiniUrus
|..|..|..Porsche911
|..|..43
|..|..|..TeslaModel3
|..|..|..31
|..|..|..|..AudiA8
|..|..|..|..Polestar2
66
|..60
|..|..BadVisibility:GoodVisibility
|..|..40
|..|..|..BadHandling:GoodHandling
|..|..|..RideVeryRough:RideVerySmooth
|..75
|..|..SimpleMaintenance:ComplexMaintenance
|..|..52
|..|..|..SeatNotComfortable:SeatVeryComfortable
|..|..|..InfotainmentHardToUse:InfotainmentEasyToUse

A TeslaModel3
B HondaCRV
C Porsche911
D AudiA8
E ToyotaCamry
F FordF150
G InfinityQ60
H Polestar2
I LamborghiniUrus
J FordMustang

[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', 'E', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'I', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', 'G', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'D', 'H', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'A', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', 'J', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']


```
