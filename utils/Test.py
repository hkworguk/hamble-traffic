# import ipykernel
# print(ipykernel.__version__)

# import sys
# print(sys.version)

# import pandas as pd
# df = pd.read_csv('data/2023/Jan/2023-01-03.csv.gz')
# print(df.columns)
# print(df.tail())

# df.to_csv('out.csv', index=False)

list_tuple = [('06:00:00', '19:00:00'), ('20:00:00', '23:00:00')]
line_styles = ['dashed', 'dashdot']
# for index, (s,e) in enumerate(list_tuple):
#     print(index)
#     print(s)
#     print(e)

journeys = [
    (
        {
            'name': 'Hamble', 'lat': 50.8599421, 'long': -1.3413876
        },
        {
            'name': 'Windhover','lat': 50.8975905, 'long': -1.3148369
        }
    ),
    (
        {
            'name': 'Hound','lat': 50.8762178,'long': -1.328644
        },
        {
            'name': 'Mallards', 'lat': 50.8826763, 'long': -1.325972,
        }
    )
]

for indes, (origin, dest) in enumerate(journeys):
    print(origin)
    print(dest)
