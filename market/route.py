from . import app, login_manager
from flask import render_template, request, redirect, url_for, jsonify
from .form import RegistrationForm, LoginForm
from .model import db, User
from flask_login import login_user, current_user, logout_user
import requests


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/profile')
def profile_page():
    return 'Profile'


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if user.check_password(form.password.data):
                    login_user(user)
                    return redirect(url_for('home_page'))
                form.new_errors = {'password': ['Not valid']}
            else:
                form.new_errors = {'username': ['not found user']}

    return render_template('sing_in.html', form=form)


@app.route('/registration', methods=['POST', 'GET'])
def registration_page():
    static = True
    form = RegistrationForm(request.form)
    # if current_user.is_authenticated:
    #     return redirect(url_for('home_page'))

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            if username and User.query.filter_by(username=username).first():
                form.new_errors = {'username': [
                    'This username exist enter other one']}
                static = False

            if not email:
                form.new_errors = {'email': ['Not valid']}
                static = False

            if not password:
                form.new_errors = {'password': ['Not valid']}
                static = False

            if static:
                u1 = User(username=username,
                          email=email,
                          password=password)

                db.session.add(u1)
                db.session.commit()
                login_user(u1)
                return redirect(url_for('home_page'))
                # 204

    return render_template('sing_up.html', form=form)


@app.route('/check-reg', methods=['POST'])
def check_user_mail():
    field_ = request.form.get('username')
    if field_:
        if User.query.filter_by(username=field_).first():
            return jsonify(result=False)

    return jsonify(result=True)


@app.route('/logout')
def logout_page():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for('login_page'))


@app.route('/recovery')
def recovery_page():
    return 'Recovery'


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404_page.html'), 404


@app.route('/games')
def games():
    return render_template('games.html')


@app.route('/one_game_page')
def one_game_page():
    return render_template('one_game_page.html')


@app.route('/trend')
def trend_page():
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ar,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json;charset=UTF-8",
        "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    }
    body = "{\"query\":\"query collectionLayoutQuery($locale: String, $country: String!, $slug: String) " \
           "{\\n  Storefront {\\n    collectionLayout(locale: $locale, slug: $slug) {\\n      _activeDate\\n      _locale\\n      _metaTags\\n      _slug\\n      _title\\n      _urlPattern\\n      lastModified\\n      regionBlock\\n      affiliateId\\n      takeover {\\n        banner {\\n          altText\\n          src\\n        }\\n        description\\n        eyebrow\\n        title\\n      }\\n      seo {\\n        title\\n        description\\n        keywords\\n        image {\\n          src\\n          altText\\n        }\\n        twitter {\\n          title\\n          description\\n        }\\n        og {\\n          title\\n          description\\n          image {\\n            src\\n            alt\\n          }\\n        }\\n      }\\n      collectionOffers {\\n        title\\n        id\\n        namespace\\n        description\\n        effectiveDate\\n        keyImages {\\n          type\\n          url\\n        }\\n        seller {\\n          id\\n          name\\n        }\\n        releaseDate\\n        prePurchase\\n        productSlug\\n        urlSlug\\n        url\\n        items {\\n          id\\n          namespace\\n        }\\n        customAttributes {\\n          key\\n          value\\n        }\\n        categories {\\n          path\\n        }\\n        linkedOfferId\\n        linkedOffer {\\n          effectiveDate\\n          customAttributes {\\n            key\\n            value\\n          }\\n        }\\n        catalogNs {\\n          mappings(pageType: \\\"productHome\\\") {\\n            pageSlug\\n            pageType\\n          }\\n        }\\n        offerMappings {\\n          pageSlug\\n          pageType\\n        }\\n        price(country: $country) {\\n          totalPrice {\\n            currencyCode\\n            currencyInfo {\\n              decimals\\n              symbol\\n            }\\n            discountPrice\\n            originalPrice\\n            voucherDiscount\\n            discount\\n            fmtPrice(locale: $locale) {\\n              originalPrice\\n              discountPrice\\n              intermediatePrice\\n            }\\n          }\\n          lineOffers {\\n            appliedRules {\\n              id\\n              endDate\\n            }\\n          }\\n        }\\n      }\\n      pageTheme {\\n        preferredMode\\n        light {\\n          theme\\n          accent\\n        }\\n        dark {\\n          theme\\n          accent\\n        }\\n      }\\n      redirect {\\n        code\\n        url\\n      }\\n    }\\n  }\\n}\\n\"," \
           "\"variables\":{\"locale\":\"ar\",\"slug\":\"top-sellers\",\"country\":\"EG\"}}"
    r = requests.post("https://www.epicgames.com/graphql", headers=headers, data=body)
    if r.ok:
        data = r.json()
        data = data.get('data',).get('Storefront',).get('collectionLayout').get('collectionOffers')
    else:
        data = {}
    return render_template('trend.html', data=data)


'''
fetch("https://www.epicgames.com/graphql", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ar,en-US;q=0.9,en;q=0.8",
    "content-type": "application/json;charset=UTF-8",
    "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
  },
  "referrer": "https://www.epicgames.com/store/ar/collection/top-sellers",
  "referrerPolicy": "no-referrer-when-downgrade",
  "body": "{\"query\":\"query collectionLayoutQuery($locale: String, $country: String!, $slug: String) {\\n  Storefront {\\n    collectionLayout(locale: $locale, slug: $slug) {\\n      _activeDate\\n      _locale\\n      _metaTags\\n      _slug\\n      _title\\n      _urlPattern\\n      lastModified\\n      regionBlock\\n      affiliateId\\n      takeover {\\n        banner {\\n          altText\\n          src\\n        }\\n        description\\n        eyebrow\\n        title\\n      }\\n      seo {\\n        title\\n        description\\n        keywords\\n        image {\\n          src\\n          altText\\n        }\\n        twitter {\\n          title\\n          description\\n        }\\n        og {\\n          title\\n          description\\n          image {\\n            src\\n            alt\\n          }\\n        }\\n      }\\n      collectionOffers {\\n        title\\n        id\\n        namespace\\n        description\\n        effectiveDate\\n        keyImages {\\n          type\\n          url\\n        }\\n        seller {\\n          id\\n          name\\n        }\\n        releaseDate\\n        prePurchase\\n        productSlug\\n        urlSlug\\n        url\\n        items {\\n          id\\n          namespace\\n        }\\n        customAttributes {\\n          key\\n          value\\n        }\\n        categories {\\n          path\\n        }\\n        linkedOfferId\\n        linkedOffer {\\n          effectiveDate\\n          customAttributes {\\n            key\\n            value\\n          }\\n        }\\n        catalogNs {\\n          mappings(pageType: \\\"productHome\\\") {\\n            pageSlug\\n            pageType\\n          }\\n        }\\n        offerMappings {\\n          pageSlug\\n          pageType\\n        }\\n        price(country: $country) {\\n          totalPrice {\\n            currencyCode\\n            currencyInfo {\\n              decimals\\n              symbol\\n            }\\n            discountPrice\\n            originalPrice\\n            voucherDiscount\\n            discount\\n            fmtPrice(locale: $locale) {\\n              originalPrice\\n              discountPrice\\n              intermediatePrice\\n            }\\n          }\\n          lineOffers {\\n            appliedRules {\\n              id\\n              endDate\\n            }\\n          }\\n        }\\n      }\\n      pageTheme {\\n        preferredMode\\n        light {\\n          theme\\n          accent\\n        }\\n        dark {\\n          theme\\n          accent\\n        }\\n      }\\n      redirect {\\n        code\\n        url\\n      }\\n    }\\n  }\\n}\\n\",\"variables\":{\"locale\":\"ar\",\"slug\":\"top-sellers\",\"country\":\"EG\"}}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});

'''
