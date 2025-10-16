from Extract import *
#from Database import *


#db="db_airport"
#csv_name="flight"
#json_name="airline"
#excel_name="airport"
#pdf_name="weather"
flights_df = extract_csv("./data/flights.csv") #données des vols
airlines_df =extract_json("./data/airlines.json") #aéroports
airports_df =extract_excel("./data/airports.xlsx") #compagnies aériennes
weather_df=extract_pdf("./data/weather.pdf") #données météo
planes_df=extract_html("./data/planes.html") #données des avions

total_airports = airports_df.shape[0]
departure_airports = flights_df['origin'].nunique()
destination_airports = flights_df['dest'].nunique()
no_dst_airports = airports_df[airports_df['dst'] != 'Y'].shape[0]
num_timezones = airports_df['tzone'].nunique()
num_airlines = airlines_df['carrier'].nunique()
num_planes = flights_df['tailnum'].nunique()
num_cancelled = flights_df[flights_df['dep_time'].isna() | flights_df['arr_time'].isna()].shape[0]
print(f"Nombre de vols annulés : {num_cancelled}")
#num_cancelled = flights_df[flights_df['cancelled'] == 1].shape[0]
#print(f"Total dest: {num_planes}")  
#connection_db = connect_db()
#connection_mydb = connect_mydb()
#rqt="""ALTER TABLE  airlines (
    #carrier varchar(2) NOT NULL,
    #name varchar(255), 
    #PRIMARY KEY (carrier)
    #);"""

#csv.to_sql(csv_name,connection_db,db)
#write_db(connection_mydb,rqt)
#json.to_sql(json_name,connection_db,db)
#excel.to_sql(excel_name,connection_db,db)
#pdf.to_sql(pdf_name,connection_db,db)

#write_db(connection,rqt)

#print(flights_df.head())    
#print(airlines_df.head())   
#print(airports_df.head())   
#print(weather_df.head())



#print(json.dtypes)
#print(excel.dtypes)
#print(pdf.dtypes)
