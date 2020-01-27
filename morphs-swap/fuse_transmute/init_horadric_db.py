from sqlalchemy import Table, Column, String, Integer, MetaData, ForeignKey


metadata = MetaData()
address_table = Table('addresses', metadata,
                      Column('postal_code', Integer, primary_key=True),
                      Column('region', String(5)),
                      Column('city', String(30))
                      )

boutiques_table = Table('boutiques', metadata,
                        Column('slug_id', String(200), primary_key=True),
                        Column('title', String(120)),
                        Column('category', String(20), index=True),
                        Column('street_address', String(60)),
                        Column('postal_code', Integer, ForeignKey('addresses.postal_code'),
                               index=True),
                        Column('reviews', Integer, index=True),
                        Column('phone', String(40)),
                        Column('comment_address', String(60)),
                        Column('image_url', String(120)),
                        Column('website', String(350)),
                        Column('schedule', String(300)),
                        Column('about', String(400)),
                        )
