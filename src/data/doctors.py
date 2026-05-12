def create_hospital(name):
    return {
        "hospital": name,
        "opening_time": "9:00 AM - 6:00 PM",
        "doctors": [
            {"name": "Dr. Oncology Specialist", "time": "10 AM - 2 PM"},
            {"name": "Dr. Cancer Consultant", "time": "3 PM - 6 PM"}
        ]
    }


DOCTORS_BY_STATE = {

"West Bengal":[
    create_hospital("Tata Medical Center, Kolkata"),
    create_hospital("AIIMS Kalyani"),
    create_hospital("Apollo Gleneagles Hospital, Kolkata")
],

"Maharashtra":[
    create_hospital("Tata Memorial Hospital, Mumbai"),
    create_hospital("Kokilaben Dhirubhai Ambani Hospital, Mumbai"),
    create_hospital("Ruby Hall Clinic, Pune")
],

"Delhi":[
    create_hospital("AIIMS Delhi"),
    create_hospital("Rajiv Gandhi Cancer Institute"),
    create_hospital("Max Super Speciality Hospital, Saket")
],

"Karnataka":[
    create_hospital("Kidwai Memorial Institute of Oncology, Bangalore"),
    create_hospital("Apollo Hospital, Bangalore"),
    create_hospital("HCG Cancer Centre, Bangalore")
],

"Tamil Nadu":[
    create_hospital("Adyar Cancer Institute, Chennai"),
    create_hospital("Apollo Cancer Centre, Chennai"),
    create_hospital("MIOT International Hospital")
],

"Telangana":[
    create_hospital("Basavatarakam Indo-American Cancer Hospital, Hyderabad"),
    create_hospital("Apollo Cancer Centre, Hyderabad"),
    create_hospital("Yashoda Hospitals, Hyderabad")
],

"Gujarat":[
    create_hospital("Gujarat Cancer Research Institute, Ahmedabad"),
    create_hospital("Apollo Hospital Ahmedabad"),
    create_hospital("HCG Cancer Centre Ahmedabad")
],

"Kerala":[
    create_hospital("Regional Cancer Centre, Thiruvananthapuram"),
    create_hospital("Amrita Hospital, Kochi"),
    create_hospital("Aster Medcity, Kochi")
],

"Punjab":[
    create_hospital("Homi Bhabha Cancer Hospital, Sangrur"),
    create_hospital("Fortis Hospital Mohali"),
    create_hospital("Dayanand Medical College, Ludhiana")
],

"Haryana":[
    create_hospital("Medanta Hospital, Gurgaon"),
    create_hospital("Artemis Hospital, Gurgaon"),
    create_hospital("Fortis Hospital Gurgaon")
],

"Rajasthan":[
    create_hospital("Bhagwan Mahaveer Cancer Hospital, Jaipur"),
    create_hospital("RCC SMS Hospital Jaipur"),
    create_hospital("Fortis Escorts Hospital Jaipur")
],

"Uttar Pradesh":[
    create_hospital("Sanjay Gandhi PGI, Lucknow"),
    create_hospital("KGMU Lucknow"),
    create_hospital("AIIMS Gorakhpur")
],

"Bihar":[
    create_hospital("Mahavir Cancer Institute, Patna"),
    create_hospital("AIIMS Patna"),
    create_hospital("Paras Hospital Patna")
],

"Assam":[
    create_hospital("Dr B Borooah Cancer Institute, Guwahati"),
    create_hospital("GNRC Hospital Guwahati"),
    create_hospital("Apollo Clinic Guwahati")
],

"Odisha":[
    create_hospital("AIIMS Bhubaneswar"),
    create_hospital("Acharya Harihar Cancer Center"),
    create_hospital("Apollo Hospital Bhubaneswar")
],

"Andhra Pradesh":[
    create_hospital("Apollo Hospital Visakhapatnam"),
    create_hospital("Andhra Hospitals Vijayawada")
],

"Arunachal Pradesh":[
    create_hospital("Tomo Riba Institute of Health")
],

"Chhattisgarh":[
    create_hospital("Balco Medical Centre, Raipur"),
    create_hospital("AIIMS Raipur")
],

"Goa":[
    create_hospital("Goa Medical College"),
    create_hospital("Manipal Hospital Goa")
],

"Himachal Pradesh":[
    create_hospital("IGMC Shimla"),
    create_hospital("AIIMS Bilaspur")
],

"Jharkhand":[
    create_hospital("Tata Main Hospital, Jamshedpur"),
    create_hospital("RIMS Ranchi")
],

"Madhya Pradesh":[
    create_hospital("AIIMS Bhopal"),
    create_hospital("Bansal Hospital, Bhopal")
],

"Manipur":[
    create_hospital("RIMS Imphal")
],

"Meghalaya":[
    create_hospital("NEIGRIHMS Shillong")
],

"Mizoram":[
    create_hospital("Civil Hospital Aizawl")
],

"Nagaland":[
    create_hospital("Naga Hospital Kohima")
],

"Sikkim":[
    create_hospital("Central Referral Hospital Gangtok")
],

"Tripura":[
    create_hospital("Agartala Govt Medical College")
],

"Uttarakhand":[
    create_hospital("AIIMS Rishikesh"),
    create_hospital("Max Hospital Dehradun")
],

"Andaman and Nicobar Islands":[
    create_hospital("GB Pant Hospital, Port Blair")
],

"Chandigarh":[
    create_hospital("PGIMER Chandigarh")
],

"Dadra and Nagar Haveli and Daman and Diu":[
    create_hospital("Silvassa Civil Hospital")
],

"Jammu and Kashmir":[
    create_hospital("SKIMS Srinagar")
],

"Ladakh":[
    create_hospital("Sonam Norboo Hospital Leh")
],

"Lakshadweep":[
    create_hospital("Indira Gandhi Hospital Kavaratti")
],

"Puducherry":[
    create_hospital("JIPMER Puducherry")
]

}