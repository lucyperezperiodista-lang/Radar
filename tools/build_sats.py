import csv, json, sys, os, glob, datetime
SAT='/home/claude/sat_in'; UCS='/home/claude/ucs_in/UCS-Satellite-Database-Interactive-Visualization/UCS Satellite Database Interactive Visualization/UCS-Satellite-Database-1-1-2023.csv'
def tle(path):
    L=[l.rstrip('\n') for l in open(path,encoding='utf-8',errors='replace') if l.strip()]
    out=[]
    for i in range(0,len(L)-2,3):
        if L[i+1].startswith('1 ') and L[i+2].startswith('2 '): out.append((L[i].strip(),L[i+1],L[i+2]))
    return out
act=tle(f'{SAT}/active.tle')
GRP={ # grupo CelesTrak -> (uso, operador/empresa)
 'starlink':('Comunicaciones (internet satelital)','SpaceX (Starlink)'),'oneweb':('Comunicaciones (internet satelital)','Eutelsat OneWeb'),
 'kuiper':('Comunicaciones (internet satelital)','Amazon (Project Kuiper)'),'qianfan':('Comunicaciones (internet satelital)','Shanghai Spacesail Technologies (Qianfan)'),
 'hulianwang':('Comunicaciones (internet satelital)','China Satellite Network Group (Guowang)'),'iridium-NEXT':('Comunicaciones','Iridium'),
 'globalstar':('Comunicaciones','Globalstar'),'orbcomm':('Comunicaciones (IoT)','ORBCOMM'),'intelsat':('Comunicaciones','Intelsat'),
 'ses':('Comunicaciones','SES'),'eutelsat':('Comunicaciones','Eutelsat'),'telesat':('Comunicaciones','Telesat'),
 'x-comm':('Comunicaciones',None),'other-comm':('Comunicaciones',None),'gps-ops':('Navegación (GPS)','Fuerza Espacial de EE. UU.'),
 'glo-ops':('Navegación (GLONASS)','Roscosmos / Rusia'),'galileo':('Navegación (Galileo)','Unión Europea (EUSPA/ESA)'),
 'beidou':('Navegación (BeiDou)','China'),'gnss':('Navegación',None),'sbas':('Navegación (aumentación)',None),'nnss':('Navegación',None),'musson':('Navegación',None),
 'weather':('Meteorología',None),'goes':('Meteorología','NOAA'),'resource':('Observación de la Tierra',None),'planet':('Observación de la Tierra','Planet Labs'),
 'spire':('Observación de la Tierra (datos meteorológicos y AIS)','Spire Global'),'dmc':('Observación de la Tierra',None),
 'science':('Ciencia',None),'geodetic':('Geodesia',None),'military':('Militar',None),'stations':('Estación espacial / tripulada',None),
 'amateur':('Radioaficionados',None),'cubesat':('Tecnología / educación',None),'education':('Educación',None),'engineering':('Ingeniería / pruebas',None),
 'sarsat':('Búsqueda y rescate',None),'argos':('Recolección de datos ambientales',None),'tdrss':('Retransmisión de datos',None),'radar':('Calibración de radar',None),
}
grp={}
for g in GRP:
    p=f'{SAT}/groups/{g}.tle'
    if os.path.exists(p):
        for nm,l1,l2 in tle(p): grp.setdefault(int(l1[2:7]),g)
# SATCAT
sc={}
for r in csv.DictReader(open(f'{SAT}/satcat.csv',encoding='utf-8')):
    try: sc[int(r['NORAD_CAT_ID'])]=r
    except: pass
# UCS
ucs={}
rows=list(csv.reader(open(UCS,encoding='latin-1')))
H=rows[0]; ix={h.strip():i for i,h in enumerate(H)}
for r in rows[1:]:
    try: n=int(r[ix['NORAD Number']].strip())
    except: continue
    g=lambda k:r[ix[k]].strip()
    ucs[n]=dict(op=g('Operator/Owner'),ct=g('Country of Operator/Owner'),us=g('Users'),pu=g('Purpose'),dp=g('Detailed Purpose'),lt=g('Expected Lifetime (yrs.)'),orb=g('Class of Orbit'))
PU={'Communications':'Comunicaciones','Earth Observation':'Observación de la Tierra','Navigation/Global Positioning':'Navegación','Navigation/Regional Positioning':'Navegación regional',
 'Technology Development':'Desarrollo tecnológico','Technology Demonstration':'Demostración tecnológica','Space Science':'Ciencia espacial','Earth Science':'Ciencias de la Tierra',
 'Space Observation':'Observación espacial','Surveillance':'Vigilancia','Educational':'Educación','Signals Intelligence':'Inteligencia de señales','Unknown':'Desconocido'}
US={'Commercial':'Comercial','Government':'Gobierno','Military':'Militar','Civil':'Civil'}
def tr(s,d):
    return '/'.join(d.get(x.strip(),x.strip()) for x in s.split('/')) if s else ''
OWN={'US':'EE. UU.','PRC':'China','CIS':'Rusia (CEI)','UK':'Reino Unido','FR':'Francia','JPN':'Japón','IND':'India','ESA':'Agencia Espacial Europea','EUME':'EUMETSAT','GER':'Alemania','CA':'Canadá','ISS':'Estación Espacial Internacional','LUXE':'Luxemburgo','ITSO':'Intelsat','SES':'SES','O3B':'O3b (SES)','EUTE':'Eutelsat','KOR':'Corea del Sur','ISRA':'Israel','IT':'Italia','SPN':'España','BRAZ':'Brasil','ARGN':'Argentina','MEX':'México','CHLE':'Chile','PER':'Perú','COL':'Colombia','BOL':'Bolivia','ECU':'Ecuador','VENZ':'Venezuela','URY':'Uruguay','PRY':'Paraguay','CRI':'Costa Rica','GUAT':'Guatemala','UAE':'Emiratos Árabes Unidos','SAUD':'Arabia Saudita','TURK':'Turquía','AUS':'Australia','NZ':'Nueva Zelanda','FIN':'Finlandia','NOR':'Noruega','SWED':'Suecia','NETH':'Países Bajos','IRAN':'Irán','TWN':'Taiwán','SING':'Singapur','INDO':'Indonesia','THAI':'Tailandia','SAFR':'Sudáfrica','NIG':'Nigeria','EGYP':'Egipto','KAZ':'Kazajistán','UKR':'Ucrania','PAKI':'Pakistán','LTU':'Lituania','POL':'Polonia','DEN':'Dinamarca','SWTZ':'Suiza','AB':'Arabsat','ORB':'ORBCOMM','GLOB':'Globalstar','IM':'Inmarsat','NICO':'Nicaragua','ITSO':'Intelsat','RWA':'Ruanda','VTNM':'Vietnam','MALA':'Malasia','PHIL':'Filipinas','NKOR':'Corea del Norte','QAT':'Catar','BGD':'Bangladés','BEL':'Bélgica','AUT':'Austria','CZE':'Chequia','GREC':'Grecia','HUN':'Hungría','PRT':'Portugal','ROM':'Rumania','EST':'Estonia','SVN':'Eslovenia','SVK':'Eslovaquia','BUL':'Bulgaria','KEN':'Kenia','GHA':'Ghana','ETH':'Etiopía','MA':'Marruecos','ALG':'Argelia','TUN':'Túnez','AZER':'Azerbaiyán','BELA':'Bielorrusia','TMMC':'Turkmenistán','MNG':'Mongolia','NPL':'Nepal','LKA':'Sri Lanka','MMR':'Myanmar','LAOS':'Laos','KAZ':'Kazajistán','JOR':'Jordania','KWT':'Kuwait','IRAQ':'Irak','BHR':'Baréin','ISRO':'India (ISRO)','IRID':'Iridium','FGER':'Francia/Alemania','FRIT':'Francia/Italia','NATO':'OTAN','SEAL':'Sea Launch','ESRO':'ESRO','RASC':'RascomStar-QAF','AC':'AsiaSat','STCT':'Singapur/Taiwán','PRES':'China/ESA','USBZ':'EE. UU./Brasil','CHBZ':'China/Brasil'}
sats=[]; stats={'ucs':0,'grp':0,'none':0}
for nm,l1,l2 in act:
    n=int(l1[2:7]); s=sc.get(n,{}); u=ucs.get(n); g=grp.get(n)
    o=dict(n=n,nm=nm,l1=l1,l2=l2)
    if s:
        o['ow']=OWN.get(s.get('OWNER',''),s.get('OWNER','')); o['ld']=s.get('LAUNCH_DATE','')
        o['ty']=s.get('OBJECT_TYPE','')
    if u:
        o['op']=u['op']; o['us']=tr(u['us'],US); o['pu']=tr(u['pu'],PU); o['lt']=u['lt']; o['src']='u'; stats['ucs']+=1
        if g: o['g']=g
    elif g:
        o['pu'],op=GRP[g]
        if op: o['op']=op
        o['g']=g; o['src']='g'; stats['grp']+=1
    else: stats['none']+=1
    sats.append(o)
ep=max(l1[18:32] for _,l1,_ in act)
meta=dict(count=len(sats),stats=stats,tle_epoch_max=ep,generated=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ'),
 sources=[{'t':'CelesTrak — elementos orbitales de satélites activos (GROUP=active), vía espejo automático satvisorcom/satvisor-data','u':'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'},
  {'t':'CelesTrak SATCAT — dueño (país u organización), fecha de lanzamiento, tipo de objeto, vía espejo astrion-tech/celestrak-mirror','u':'https://celestrak.org/satcat/search.php'},
  {'t':'Union of Concerned Scientists, UCS Satellite Database (edición 1 ene 2023): operador, usuarios, propósito, vida útil esperada','u':'https://www.ucs.org/resources/satellite-database'},
  {'t':'Grupos temáticos de CelesTrak (Starlink, OneWeb, Kuiper, GPS, meteorología, etc.): uso y operador cuando el satélite no está en la base UCS','u':'https://celestrak.org/NORAD/elements/'}])
out=sys.argv[1]
json.dump(dict(meta=meta,sats=sats),open(out,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print(meta['count'],stats,ep,os.path.getsize(out))
