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
  if multi_proprietors == 'TwoPI'
    multiple_proprietors_json = ",{
    \"addresses\": [
      {
        \"postal_county\": \"London\",
        \"address_string\":  \"#{house_no}, #{street_name}, #{town} #{postcode}\",
        \"address_type\": \"UK\",
        \"auto_uppercase_override\": true
      }
    ],
    \"name\": {
      \"surname\": \"#{surname}\",
      \"forename\": \"#{forename}\",
      \"name_category\": \"#{name_category}\",
      \"auto_uppercase_override\": true
    }
  }"
  elsif multi_proprietors == 'OnePIOneCharity'
    multiple_proprietors_json = "PlaceHolder"
  else
    multiple_proprietors_json = ""
  end

  create_title_sql = <<-eos
INSERT INTO "title_register_data" ("title_number", "register_data", "geometry_data") VALUES (
  '#{title_number}',
  '{
          "application_reference": "MA2784E",
          "class": "Absolute",
          "districts": [
              "LUTON"
          ],
          "dlr": "Peterborough Office",
          "edition_date": "2014-05-22",
          "filed_plan_format": "VECTOR",
          "groups": [
              {
                  "category": "PROPERTY",
                  "entries": [
                      {
                          "category": "PROPERTY",
                          "entry_date": "2014-05-22",
                          "entry_id": "2014-05-22 15:39:52.527610",
                          "full_text": "#{full_text}",
                          "infills": [
                              {
                                  "address": {
                                      "address_string": "#{house_no} #{street_name}, #{town} (#{postcode})",
                                      "postcode": "#{postcode}",
                                      "town": "#{town}",
                                      "house_no": "#{house_no}",
                                      "street_name": "#{street_name}"
                                  },
                                  "type": "Address"
                              }
                          ],
                          "language": "ENG",
                          "role_code": "RDES",
                          "sequence_number": 1,
                          "status": "Current",
                          "sub_register": "A",
                          "template_text": "The Freehold land shown edged with red on the plan of the above title filed at the Registry and being *AD*"
                      }
                  ]
              },
              {
                  "category": "OWNERSHIP",
                  "entries": [
                      {
                          "category": "OWNERSHIP",
                          "entry_date": "2014-05-22",
                          "entry_id": "2014-05-22 15:39:32.607710",
                          "full_text": "#{full_text}",
                          "infills": [
                              {
                                  "proprietors": [
                                      {
                                          "addresses": [
                                              {
                                                  "address_string":  "#{house_no}, #{street_name}, #{town} #{postcode}",
                                                  "address_type": "UK",
                                                  "house_no": "#{house_no}",
                                                  "postcode": "#{postcode}",
                                                  "street_name": "#{street_name}",
                                                  "town": "#{town}"
                                              }
                                          ],
                                          "name": {
                                            "surname": "#{surname}",
                                            "forename": "#{forename}",
                                            "name_category": "#{name_category}"
                                          }
                                      }
                                      #{multiple_proprietors_json}
                                  ],
                                  "type": "Proprietor"
                              }
                          ],
                          "language": "ENG",
                          "role_code": "RPRO",
                          "sequence_number": 1,
                          "status": "Current",
                          "sub_register": "B",
                          "template_text": "PROPRIETOR: *RP*"
                      },
                      {
                          "category": "OWNERSHIP",
                          "draft_entry_code": "BK688",
                          "draft_entry_version": 1,
                          "entry_date": "2014-05-22",
                          "entry_id": "2014-05-22 15:38:01.287620",
                          "full_text": "The price stated to have been paid on 1 May 2014 was £100,000.",
                          "infills": [
                              {
                                  "date": "2014-05-01",
                                  "text": "01/05/2014",
                                  "type": "DATE"
                              },
                              {
                                  "text": "£100,000",
                                  "type": "PRICE"
                              }
                          ],
                          "language": "ENG",
                          "role_code": "RPPD",
                          "sequence_number": 2,
                          "status": "Current",
                          "sub_register": "B",
                          "template_text": "The price stated to have been paid on *DA* was *AM*."
                      }
                  ]
              }
          ],
          "last_app_timestamp": "2014-08-28T12:37:13+01:00",
          "tenure": "Freehold",
          "title_number": "DN1000",
          "uprns": [
              1068558627
          ]
      }',
  '{"geometry_data": {
      "geometry": {
          "extent": {
              "crs": {
                  "properties": {
                      "name": "urn:ogc:def:crs:EPSG::27700"
                  },
                  "type": "name"
              },
              "geometry": {
                  "coordinates": [
                      [
                          [
                              508263.97,
                              221692.13
                          ],
                          [
                              508266.4,
                              221698.84
                          ],
                          [
                              508266.35,
                              221700.25
                          ],
                          [
                              508270.3,
                              221711.15
                          ],
                          [
                              508273.29,
                              221719.53
                          ],
                          [
                              508271.4,
                              221721.65
                          ],
                          [
                              508270.68,
                              221722.44
                          ],
                          [
                              508269.69,
                              221723.53
                          ],
                          [
                              508263.58,
                              221706.87
                          ],
                          [
                              508261.346,
                              221700.587
                          ],
                          [
                              508258.98,
                              221693.93
                          ],
                          [
                              508258.01,
                              221691.18
                          ],
                          [
                              508262,
                              221689.66
                          ],
                          [
                              508262.95,
                              221689.3
                          ],
                          [
                              508263.97,
                              221692.13
                          ]
                      ]
                  ],
                  "type": "Polygon"
              },
              "properties": {
                  "colour": 17,
                  "feature_id": 4013,
                  "graphic_type": "Bordered Polygon",
                  "render_attributes": {
                      "border_colour": 17,
                      "border_width": 1000,
                      "exterior_edge_colour": 17,
                      "exterior_edge_thickness": 1,
                      "exterior_edge_thickness_units": "Pixels",
                      "fill_colour": 28,
                      "fill_style": 0,
                      "render_level": "0"
                  },
                  "width": 1000
              },
              "type": "Feature"
          },
          "index": {
              "crs": {
                  "properties": {
                      "name": "urn:ogc:def:crs:EPSG::27700"
                  },
                  "type": "name"
              },
              "geometry": {
                  "coordinates": [
                      [
                          [
                              508263.97,
                              221692.13
                          ],
                          [
                              508266.4,
                              221698.84
                          ],
                          [
                              508266.35,
                              221700.25
                          ],
                          [
                              508270.3,
                              221711.15
                          ],
                          [
                              508273.29,
                              221719.53
                          ],
                          [
                              508271.4,
                              221721.65
                          ],
                          [
                              508270.68,
                              221722.44
                          ],
                          [
                              508269.69,
                              221723.53
                          ],
                          [
                              508263.58,
                              221706.87
                          ],
                          [
                              508258.98,
                              221693.93
                          ],
                          [
                              508258.01,
                              221691.18
                          ],
                          [
                              508262,
                              221689.66
                          ],
                          [
                              508262.95,
                              221689.3
                          ],
                          [
                              508263.97,
                              221692.13
                          ]
                      ]
                  ],
                  "type": "Polygon"
              },
              "properties": {
                  "colour": 25,
                  "feature_id": 4019,
                  "graphic_type": "Bordered Polygon",
                  "render_attributes": {
                      "border_colour": 25,
                      "border_width": 0,
                      "exterior_edge_colour": 1,
                      "exterior_edge_thickness": 2,
                      "exterior_edge_thickness_units": "Pixels",
                      "fill_colour": 25,
                      "fill_style": 9,
                      "render_level": "0"
                  },
                  "width": 0
              },
              "type": "Feature"
          },
          "map": {
              "crs": {
                  "properties": {
                      "name": "urn:ogc:def:crs:EPSG::27700"
                  },
                  "type": "name"
              },
              "features": [
                  {
                      "geometry": {
                          "coordinates": [
                              [
                                  508235.35,
                                  221720.2
                              ],
                              [
                                  508230.9,
                                  221712.5
                              ]
                          ],
                          "type": "LineString"
                      },
                      "properties": {
                          "feature_id": 10018,
                          "graphic_type": "Poly Line",
                          "render_attributes": {
                              "render_level": "0"
                          }
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508296.75,
                              221743.4
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10169,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": null,
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": null,
                              "text_vertical_alignment": "Middle"
                          },
                          "rotation": -0.9705304697353966,
                          "value": "AVONDALE ROAD",
                          "vertical_alignment": "Middle"
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508298.7,
                              221672.85
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10169,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": null,
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": null,
                              "text_vertical_alignment": "Middle"
                          },
                          "rotation": -0.2810061055808009,
                          "value": "HAZELBURY CRESCENT",
                          "vertical_alignment": "Middle"
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508261.71,
                              221765.2
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10026,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": "Left",
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": "Left",
                              "text_vertical_alignment": "Baseline"
                          },
                          "rotation": 2.1307951881723985,
                          "value": "35",
                          "vertical_alignment": "Baseline"
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508259.63,
                              221763.9
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10026,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": "Left",
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": "Left",
                              "text_vertical_alignment": "Baseline"
                          },
                          "rotation": 2.1307951881723985,
                          "value": "33",
                          "vertical_alignment": "Baseline"
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508257.48,
                              221762.54
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10026,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": "Left",
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": "Left",
                              "text_vertical_alignment": "Baseline"
                          },
                          "rotation": 2.1307951881723985,
                          "value": "31",
                          "vertical_alignment": "Baseline"
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508302.6,
                              221662.6
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10026,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": "Centre",
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": "Centre",
                              "text_vertical_alignment": "Baseline"
                          },
                          "rotation": 2.9999870521081,
                          "value": "21",
                          "vertical_alignment": "Baseline"
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508282.3,
                              221747.9
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10026,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": "Centre",
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": "Centre",
                              "text_vertical_alignment": "Baseline"
                          },
                          "rotation": 2.205960246778795,
                          "value": "27",
                          "vertical_alignment": "Baseline"
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508223.04,
                              221718.34
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10026,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": "Left",
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": "Left",
                              "text_vertical_alignment": "Baseline"
                          },
                          "rotation": 2.6231071472844465,
                          "value": "1 to 8",
                          "vertical_alignment": "Baseline"
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508222.34,
                              221738.99
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10026,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": "Left",
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": "Left",
                              "text_vertical_alignment": "Baseline"
                          },
                          "rotation": 0,
                          "value": "Hazelbury",
                          "vertical_alignment": "Baseline"
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508287.9,
                              221685.45
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10026,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": "Centre",
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": "Centre",
                              "text_vertical_alignment": "Baseline"
                          },
                          "rotation": -0.26892600687620144,
                          "value": "6",
                          "vertical_alignment": "Baseline"
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508266.35,
                              221750.95
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10026,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": "Centre",
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": "Centre",
                              "text_vertical_alignment": "Baseline"
                          },
                          "rotation": -0.9478083793148405,
                          "value": "1 to 6",
                          "vertical_alignment": "Baseline"
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508311.3,
                              221738.9
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10026,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": "Centre",
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": "Centre",
                              "text_vertical_alignment": "Baseline"
                          },
                          "rotation": -0.9829940636369674,
                          "value": "30",
                          "vertical_alignment": "Baseline"
                      },
                      "type": "Feature"
                  },
                  {
                      "geometry": {
                          "coordinates": [
                              508238.3,
                              221682.4
                          ],
                          "type": "Point"
                      },
                      "properties": {
                          "feature_id": 10026,
                          "graphic_type": "Text",
                          "height": 1000,
                          "horizontal_alignment": "Centre",
                          "render_attributes": {
                              "render_level": "0",
                              "text_horizontal_alignment": "Centre",
                              "text_vertical_alignment": "Baseline"
                          },
                          "rotation": 2.773053769300268,
                          "value": "47",
                          "vertical_alignment": "Baseline"
                      },
                      "type": "Feature"
                  }
              ],
              "properties": {
                  "map_reference": "TL0821NW",
                  "orientation_code": "P",
                  "print_size": "A4",
                  "scale": "500  ",
                  "stamp_code_1": " ",
                  "stamp_code_2": " ",
                  "stamp_code_3": " ",
                  "stamp_code_4": " ",
                  "stamp_code_5": " ",
                  "stamp_text_1": " ",
                  "stamp_text_2": " ",
                  "stamp_text_3": " ",
                  "stamp_text_4": " ",
                  "stamp_text_5": " "
              },
              "type": "FeatureCollection"
          },
          "references": [
              {
                  "crs": {
                      "properties": {
                          "name": "urn:ogc:def:crs:EPSG::27700"
                      },
                      "type": "name"
                  },
                  "features": [
                      {
                          "geometry": {
                              "coordinates": [
                                  [
                                      508264.15,
                                      221699.65
                                  ],
                                  [
                                      508261.346,
                                      221700.587
                                  ]
                              ],
                              "type": "LineString"
                          },
                          "properties": {
                              "feature_id": 4002,
                              "graphic_type": "Poly Line",
                              "render_attributes": {
                                  "edge_colour": 7,
                                  "edge_style": 7,
                                  "edge_thickness": 1,
                                  "render_level": "0"
                              }
                          },
                          "type": "Feature"
                      }
                  ],
                  "properties": {
                      "colour_code": 2,
                      "description": "black pecked line",
                      "graphic_code": 2,
                      "text_code": 0
                  },
                  "type": "FeatureCollection"
              },
              {
                  "crs": {
                      "properties": {
                          "name": "urn:ogc:def:crs:EPSG::27700"
                      },
                      "type": "name"
                  },
                  "features": [
                      {
                          "geometry": {
                              "coordinates": [
                                  [
                                      [
                                          508264.15,
                                          221699.65
                                      ],
                                      [
                                          508266.35,
                                          221705.9
                                      ],
                                      [
                                          508263.58,
                                          221706.87
                                      ],
                                      [
                                          508261.346,
                                          221700.587
                                      ],
                                      [
                                          508264.15,
                                          221699.65
                                      ]
                                  ]
                              ],
                              "type": "Polygon"
                          },
                          "properties": {
                              "colour": 0,
                              "feature_id": 4011,
                              "graphic_type": "Bordered Polygon",
                              "render_attributes": {
                                  "border_colour": 0,
                                  "border_width": 0,
                                  "exterior_edge_colour": 9,
                                  "exterior_edge_thickness": 1,
                                  "exterior_edge_thickness_units": "Pixels",
                                  "fill_colour": 28,
                                  "fill_style": 9,
                                  "render_level": "0"
                              },
                              "width": 0
                          },
                          "type": "Feature"
                      }
                  ],
                  "properties": {
                      "colour_code": 5,
                      "description": "tinted blue",
                      "graphic_code": 15,
                      "text_code": 0
                  },
                  "type": "FeatureCollection"
              }
          ]
      }
   }
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
  #multi_proprietors = title_data[:multi_proprietors]

  create_title_sql = <<-eos
INSERT INTO "title_register_data" ("title_number", "register_data", "geometry_data") VALUES (
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
     ]
    }',
  '{"geometry": {
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


=begin


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




=end
end

# connect to the database and execute the sql (that deletes everything)
def delete_all_titles
  $db_connection.exec("DELETE FROM title_register_data;")
end
