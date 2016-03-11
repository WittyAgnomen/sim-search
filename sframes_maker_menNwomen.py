#script for creating men and women sframe


import graphlab as gl
macy=gl.SFrame('./mergefef.gl/')
sf  = gl.SFrame.read_csv('pfeats.csv')
sf=sf.rename({'X1':'n'})
sf['n']=sf['n'].apply(lambda x: x.split('/')[-1])
sf['n']=sf['n'].apply(lambda x: x.replace('.jpg',''))
sf=sf.unique()
sf.__materialize__()
men=macy[['cat','n']]
men['cat']=men['cat'].apply(lambda x:None if x=='women' else x)
men=men.dropna('cat')
men.__materialize__()
men=men.join(sf, on='n', how='left')
men.save('./menpf.gl/')

women=macy[['cat','n']]
women['cat']=women['cat'].apply(lambda x:None if x=='men' else x)
women=women.dropna('cat')
women.__materialize__()
women=women.join(sf, on='n', how='left')
women.__materialize__()
women.save('./womenpf.gl/')
