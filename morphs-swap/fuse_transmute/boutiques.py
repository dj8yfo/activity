from itertools import filterfalse
import re


class Boutique(object):

    def __init__(self, slug, street_address=None,
                 comment_address=None, postal_code=None,
                 category=None, title=None, phone=None,
                 image_url=None, reviews=None, website=None,
                 schedule=None, about=None, **kwargs):
        self.slug_id = slug
        self.street_address = street_address
        self.comment_address = comment_address
        self.postal_code = postal_code
        self.category = category
        self.title = title
        self.phone = phone
        self.image_url = image_url
        self.reviews = reviews
        self.website = website
        self.schedule = schedule
        self.about = about

    def __repr__(self):
        return f'boutique("{self.slug_id}", {self.postal_code},' +\
            f' "{self.street_address}", "{self.comment_address}", ' +\
            f' {self.reviews})'

    @classmethod
    def from_kadmin(cls, argdict):
        pattern = re.compile(r'''
            ^
            .*
            /biz/
            (.*)      # slug_id  group
            \?osq=.*
            ''', re.VERBOSE)
        slug_id = pattern.search(argdict['url']).groups()[0]
        pattern = re.compile(r'''
            ^
            \D*
            (\d+)    # num reviews group
            .*
            ''', re.VERBOSE)
        match = pattern.search(argdict['reviews_str'])
        reviews = int(match.groups()[0]) if match else None
        addresses = argdict['addresses']
        street_address = addresses[0]
        comment_address = None
        if len(addresses) == 3:
            comment_address = addresses[1]
        _, _, pc = GoPostalMode.postal_components(addresses[-1])
        image_url = argdict['image_url_raw'][:119]
        website = argdict['website_raw'][:349]
        schedule = argdict['schedule_raw'][:299]
        about = argdict['about_raw'][:399]
        return cls(slug_id, street_address=street_address, comment_address=comment_address,
                   postal_code=pc, reviews=reviews, website=website,
                   schedule=schedule, about=about, image_url=image_url, **argdict)


class GoPostalMode(object):
    def __init__(self, postal_code, region=None, city=None, **kwargs):
        self.postal_code = postal_code
        self.region = region
        self.city = city

    def __repr__(self):
        return f'location( {self.postal_code}, "{self.city}", "{self.region}")'

    @classmethod
    def postal_components(cls, combo_str):
        city, subcombo = combo_str.strip().split(',')
        region, pc = subcombo.strip().split()
        return (city, region, int(pc))

    @classmethod
    def from_kadmin(cls, argdict):
        addresses = argdict['addresses']
        city, region, pc = cls.postal_components(addresses[-1])
        return cls(pc, region, city)


def removeNone(arg):
    return dict(filterfalse(lambda x: x[1] is None, arg.items()))


if __name__ == '__main__':
    # bout = Boutique(**dic)
    # postal = GoPostalMode(**dic)

    # print(bout)
    # print(postal)

    argdict = {
        'url': "https://testkit/biz/philz-coffee-san-francisco-16?osq=restaurants",
        'addresses': [
            "8635 West 3rd St",
            "Ste 1090W",
            "Los Angeles, CA 90048"
        ],
        'reviews_str': '117 reviews'
    }
    argdict1 = {
        'url': "https://testkit/biz/bay-area-professionals-fitness-and-wellness-san-francisco-3?osq=gyms",
        'addresses': [
            "290 Division St",
            "Ste 200",
            "San Francisco, CA 94103"
        ],
        'reviews_str': '18934 reviews'
    }

    for arg in [argdict, argdict1]:
        print(arg)
        print(GoPostalMode.from_kadmin(arg))
        print(Boutique.from_kadmin(arg))
