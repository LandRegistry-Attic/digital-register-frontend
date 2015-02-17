def create_title_in_db(title_data)

  title_number = title_data[:title_number]
  postcode = title_data[:postcode]
  street_name = title_data[:street_name]
  house_no = title_data[:house_no]
  town = title_data[:town]

  create_title_sql = <<-eos
INSERT INTO "title_register_data" ("title_number", "register_data", "geometry_data") VALUES (
  '#{title_number}',
  '{
  "last_app_timestamp": "2014-08-28T12:37:13+01:00",
  "filed_plan_format": "EXAMPLE_filed_plan_format",
  "edition_date": "EXAMPLE_edition_date",
  "class": "EXAMPLE_class",
  "entries": [
    {
      "entry_id": "EXAMPLE_entry_id",
      "sub_register": "EXAMPLE_sub_register",
      "schedule": {
        "fields": [
          {
            "text": "EXAMPLE_text",
            "parties": [
              {
                "names": [
                  {
                    "country_incorporation": "EXAMPLE_country_incorporation",
                    "company_reg_num": "EXAMPLE_company_reg_num",
                    "name_information": "EXAMPLE_name_information",
                    "alias_names": [
                      {
                        "upper_override": "EXAMPLE_upper_override",
                        "surname": "EXAMPLE_surname",
                        "title": "EXAMPLE_title",
                        "decoration": "EXAMPLE_decoration",
                        "forename": "EXAMPLE_forename"
                      }
                    ],
                    "name_occupation": "EXAMPLE_name_occupation",
                    "surname": "EXAMPLE_surname",
                    "name_supplimentary": "EXAMPLE_name_supplimentary",
                    "trading_name": "EXAMPLE_trading_name",
                    "trust_format": "EXAMPLE_trust_format",
                    "decoration": "EXAMPLE_decoration",
                    "forename": "EXAMPLE_forename",
                    "name_category": "EXAMPLE_name_category",
                    "charity_name": "EXAMPLE_charity_name",
                    "local_authority_area": "EXAMPLE_local_authority_area",
                    "title": "EXAMPLE_title",
                    "company_location": "EXAMPLE_company_location",
                    "auto_uppercase_override": "EXAMPLE_auto_uppercase_override",
                    "non_private_individual_name": "EXAMPLE_non_private_individual_name"
                  }
                ],
                "party_role_description": "EXAMPLE_party_role_description"
              }
            ],
            "header": "EXAMPLE_header"
          }
        ],
        "schedule_type": "EXAMPLE_schedule_type",
        "parent_register": "EXAMPLE_parent_register",
        "header": "EXAMPLE_header"
      },
      "deeds": [
        {
          "rent_detail": "EXAMPLE_rent_detail",
          "parties": [
            {
              "names": [
                {
                  "country_incorporation": "EXAMPLE_country_incorporation",
                  "company_reg_num": "EXAMPLE_company_reg_num",
                  "name_information": "EXAMPLE_name_information",
                  "alias_names": [
                    {
                      "upper_override": "EXAMPLE_upper_override",
                      "surname": "EXAMPLE_surname",
                      "title": "EXAMPLE_title",
                      "decoration": "EXAMPLE_decoration",
                      "forename": "EXAMPLE_forename"
                    }
                  ],
                  "name_occupation": "EXAMPLE_name_occupation",
                  "surname": "EXAMPLE_surname",
                  "name_supplimentary": "EXAMPLE_name_supplimentary",
                  "trading_name": "EXAMPLE_trading_name",
                  "trust_format": "EXAMPLE_trust_format",
                  "decoration": "EXAMPLE_decoration",
                  "forename": "EXAMPLE_forename",
                  "name_category": "EXAMPLE_name_category",
                  "charity_name": "EXAMPLE_charity_name",
                  "local_authority_area": "EXAMPLE_local_authority_area",
                  "title": "EXAMPLE_title",
                  "company_location": "EXAMPLE_company_location",
                  "auto_uppercase_override": "EXAMPLE_auto_uppercase_override",
                  "non_private_individual_name": "EXAMPLE_non_private_individual_name"
                }
              ],
              "party_role_description": "EXAMPLE_party_role_description"
            }
          ],
          "rentcharge_amount": "EXAMPLE_rentcharge_amount",
          "date": "EXAMPLE_date",
          "title_number": "EXAMPLE_title_number",
          "payment_detail": "EXAMPLE_payment_detail",
          "lease_term": "EXAMPLE_lease_term",
          "description": "EXAMPLE_description"
        }
      ],
      "status": "EXAMPLE_status",
      "role_code": "RDES",
      "draft_entry_version": "EXAMPLE_draft_entry_version",
      "language": "EXAMPLE_language",
      "infills": [
        {
          "address": {
            "postcode": "#{postcode}",
            "region_name": "EXAMPLE_region_name",
            "sub_building_description": "EXAMPLE_sub_building_description",
            "trail_info": "EXAMPLE_trail_info",
            "sub_building_no": "EXAMPLE_sub_building_no",
            "plot_no": "EXAMPLE_plot_no",
            "secondary_house_alpha": "EXAMPLE_secondary_house_alpha",
            "postal_county": "EXAMPLE_postal_county",
            "town": "#{town}",
            "local_name": "EXAMPLE_local_name",
            "dx_no": "EXAMPLE_dx_no",
            "care_of_name": "EXAMPLE_care_of_name",
            "address_string": "EXAMPLE_address_string",
            "leading_info": "EXAMPLE_leading_info",
            "house_alpha": "EXAMPLE_house_alpha",
            "plot_code": "EXAMPLE_plot_code",
            "secondary_house_no": "EXAMPLE_secondary_house_no",
            "email_address": "EXAMPLE_email_address",
            "house_no": "#{house_no}",
            "address_type": "EXAMPLE_address_type",
            "exchange_name": "EXAMPLE_exchange_name",
            "country": "EXAMPLE_country",
            "street_name": "#{street_name}",
            "care_of": "EXAMPLE_care_of",
            "auto_uppercase_override": "EXAMPLE_auto_uppercase_override",
            "house_description": "EXAMPLE_house_description"
          },
          "text": "EXAMPLE_text",
          "date": "EXAMPLE_date",
          "charge": [
            {
              "charge_date": "EXAMPLE_charge_date"
            }
          ],
          "proprietors": [
            {
              "addresses": [
                {
                  "postcode": "EXAMPLE_postcode",
                  "region_name": "EXAMPLE_region_name",
                  "sub_building_description": "EXAMPLE_sub_building_description",
                  "trail_info": "EXAMPLE_trail_info",
                  "sub_building_no": "EXAMPLE_sub_building_no",
                  "plot_no": "EXAMPLE_plot_no",
                  "secondary_house_alpha": "EXAMPLE_secondary_house_alpha",
                  "postal_county": "EXAMPLE_postal_county",
                  "town": "EXAMPLE_town",
                  "local_name": "EXAMPLE_local_name",
                  "dx_no": "EXAMPLE_dx_no",
                  "care_of_name": "EXAMPLE_care_of_name",
                  "address_string": "EXAMPLE_address_string",
                  "leading_info": "EXAMPLE_leading_info",
                  "house_alpha": "EXAMPLE_house_alpha",
                  "plot_code": "EXAMPLE_plot_code",
                  "secondary_house_no": "EXAMPLE_secondary_house_no",
                  "email_address": "EXAMPLE_email_address",
                  "house_no": "EXAMPLE_house_no",
                  "address_type": "EXAMPLE_address_type",
                  "exchange_name": "EXAMPLE_exchange_name",
                  "country": "EXAMPLE_country",
                  "street_name": "EXAMPLE_street_name",
                  "care_of": "EXAMPLE_care_of",
                  "auto_uppercase_override": "EXAMPLE_auto_uppercase_override",
                  "house_description": "EXAMPLE_house_description"
                }
              ],
              "trustee": "EXAMPLE_trustee",
              "name": {
                "country_incorporation": "EXAMPLE_country_incorporation",
                "company_reg_num": "EXAMPLE_company_reg_num",
                "name_information": "EXAMPLE_name_information",
                "alias_names": [
                  {
                    "upper_override": "EXAMPLE_upper_override",
                    "surname": "EXAMPLE_surname",
                    "title": "EXAMPLE_title",
                    "decoration": "EXAMPLE_decoration",
                    "forename": "EXAMPLE_forename"
                  }
                ],
                "name_occupation": "EXAMPLE_name_occupation",
                "surname": "EXAMPLE_surname",
                "name_supplimentary": "EXAMPLE_name_supplimentary",
                "trading_name": "EXAMPLE_trading_name",
                "trust_format": "EXAMPLE_trust_format",
                "decoration": "EXAMPLE_decoration",
                "forename": "EXAMPLE_forename",
                "name_category": "EXAMPLE_name_category",
                "charity_name": "EXAMPLE_charity_name",
                "local_authority_area": "EXAMPLE_local_authority_area",
                "title": "EXAMPLE_title",
                "company_location": "EXAMPLE_company_location",
                "auto_uppercase_override": "EXAMPLE_auto_uppercase_override",
                "non_private_individual_name": "EXAMPLE_non_private_individual_name"
              },
              "type": "EXAMPLE_type"
            }
          ],
          "type": "EXAMPLE_type"
        }
      ],
      "entry_date": "EXAMPLE_entry_date",
      "full_text": "EXAMPLE_full_text",
      "notes": [
        {
          "text": "EXAMPLE_text",
          "font": "EXAMPLE_font"
        }
      ],
      "template_text": "EXAMPLE_template_text",
      "draft_entry_code": "EXAMPLE_draft_entry_code"
    }
  ],
  "title_number": "EXAMPLE_title_number",
  "dlr": "EXAMPLE_dlr",
  "application_reference": "EXAMPLE_application_reference",
  "tenure": "EXAMPLE_tenure",
  "raster_plan_quality": "EXAMPLE_raster_plan_quality",
  "uprns": [
    "EXAMPLE_uprn"
  ],
  "migration_errors": [
    {
      "extractor": "EXAMPLE_extractor",
      "message_number": "EXAMPLE_message_number",
      "entry_id": "EXAMPLE_entry_id",
      "message": "EXAMPLE_message"
    }
  ],
  "districts": [
    "EXAMPLE_district"
  ]
}

',
'{
    "map": {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          0.0,
          0.0
        ]
      },
      "properties": {

      },
      "crs": {
        "type": "name",
        "properties": {
          "name": "urn:ogc:def:crs:EPSG::27700"
        }
      }
    },
    "extent": {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          0.0,
          0.0
        ]
      },
      "properties": {

      },
      "crs": {
        "type": "name",
        "properties": {
          "name": "urn:ogc:def:crs:EPSG::27700"
        }
      }
    },
    "index": {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          0.0,
          0.0
        ]
      },
      "properties": {

      },
      "crs": {
        "type": "name",
        "properties": {
          "name": "urn:ogc:def:crs:EPSG::27700"
        }
      }
    },
    "references": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [
            0.0,
            0.0
          ]
        },
        "properties": {

        },
        "crs": {
          "type": "name",
          "properties": {
            "name": "urn:ogc:def:crs:EPSG::27700"
          }
        }
      }
    ]
  }'
);
eos

  # calls the database conection - settings in the config.rb
  # and executes the create property sql
  $db_connection.exec(create_title_sql)
end

def create_proprietor_title_in_db(title_data)

  title_number = title_data[:title_number]
  postcode = title_data[:postcode]
  street_name = title_data[:street_name]
  house_no = title_data[:house_no]
  town = title_data[:town]
  surname = title_data[:surname]
  forename = title_data[:forename]
  name_category = title_data[:name_category]
  full_text = title_data[:full_text]
  multi_proprietors = title_data[:multi_proprietors]

  create_title_sql = <<-eos
INSERT INTO "title_register_data" ("title_number", "register_data") VALUES (
  '#{title_number}',
  '{
     "filed_plan_format": "PAPER",
     "edition_date": "2003-07-25",
     "last_app_timestamp": "2003-07-25T16:20:01+01:00",
     "class": "Absolute",
     "title_number": "AV239038",
     "dlr": "Gloucester Office",
     "application_reference": "F737RBF",
     "groups": [
       {
         "category": "PROPERTY",
         "entries": [
           {
             "entry_id": "2015-02-03 12:48:29.760945",
             "sub_register": "A",
             "status": "Current",
             "sequence_number": 1,
             "role_code": "RDES",
             "language": "ENG",
             "category": "PROPERTY",
             "infills": [
               {
                 "address": {
                   "address_string": "the Incorporeal hereditaments known as The Manor or Lordship or Reputed Manor or Lordship of Littleton-upon-Severn in the former Parish of Littleton-upon-Severn",
                   "auto_uppercase_override": true
                 },
                 "type": "Address"
               }
             ],
             "full_text": "The Freehold land being the Incorporeal hereditaments known as The Manor or Lordship or Reputed Manor or Lordship of Littleton-upon-Severn in the former Parish of Littleton-upon-Severn.",
             "entry_date": "1994-05-25",
             "template_text": "The Freehold land being *AD*"
           }
         ]
       },
       {
         "category": "OWNERSHIP",
         "entries": [
           {
             "entry_id": "2015-02-03 12:48:31.495975",
             "sub_register": "B",
             "status": "Current",
             "sequence_number": 1,
             "role_code": "RPRO",
             "language": "ENG",
             "category": "OWNERSHIP",
             "infills": [
               {
                 "proprietors": [
                   {
                     "addresses": [
                       {
                         "postal_county": "London",
                         "address_string":  "#{house_no}, #{street_name}, #{town} #{postcode}",
                         "address_type": "UK",
                         "auto_uppercase_override": true
                       }
                     ],
                     "name": {
                       "surname": "#{surname}",
                       "forename": "#{forename}",
                       "name_category": "#{name_category}",
                       "auto_uppercase_override": true
                     }
                   }
                   #{if multi_proprietors
                   ',{
                     "addresses": [
                       {
                         "postal_county": "London",
                         "address_string":  "#{house_no}, #{street_name}, #{town} #{postcode}",
                         "address_type": "UK",
                         "auto_uppercase_override": true
                       }
                     ],
                     "name": {
                       "surname": "#{surname}",
                       "forename": "#{forename}",
                       "name_category": "#{name_category}",
                       "auto_uppercase_override": true
                     }
                   }'}
                 ],
                 "type": "Proprietor"
               }
             ],
             "full_text": "#{full_text}",
             "entry_date": "2003-07-25",
             "template_text": "PROPRIETOR: *RP*"
           }
         ]
       }
     ],
     "geometry": {

     },
     "tenure": "Freehold",
     "raster_plan_quality": "INSUFFICIENT",
     "migration_errors": [
       {
         "extractor": "Register Check",
         "message_number": "RC1026",
         "message": "Title is not synchronised"
       },
       {
         "extractor": "Register Metadata",
         "message_number": "RC1043",
         "message": "No UPRN rows found for title"
       },
       {
         "extractor": "Property Extractor",
         "message_number": "PE1012",
         "entry_id": "2015-02-03 12:48:29.760945",
         "message": "Address not deconstructed in Intelligent Register for title"
       },
       {
         "extractor": "Geometry Extractor",
         "message_number": "GE1066",
         "message": "File Plan not vectorised"
       },
       {
         "extractor": "Geometry Extractor",
         "message_number": "GE1053",
         "message": "Title not on index map"
       },
       {
         "extractor": "Geometry Extractor",
         "message_number": "GE1006",
         "message": "No Extent or Index Generated"
       }
     ],
     "districts": [
       "SOUTH GLOUCESTERSHIRE"
     ]
   }'
);
eos

  # calls the database conection - settings in the config.rb
  # and executes the create property sql
  $db_connection.exec(create_title_sql)
end

# connect to the database and execute the sql (that deletes everything)
def delete_all_titles
  $db_connection.exec("DELETE FROM title_register_data;")
end
