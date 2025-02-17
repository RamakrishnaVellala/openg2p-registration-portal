import logging
from argparse import _AppendAction

from werkzeug.exceptions import Forbidden, Unauthorized

from odoo import _, http
from odoo.http import request

from odoo.addons.web.controllers.home import Home

_logger = logging.getLogger(__name__)


class PortalBaseController(http.Controller):
    @http.route(["/portal"], type="http", auth="public", website=True)
    def portal_root(self, **kwargs):
        if request.session and request.session.uid:
            return request.redirect("/portal/home")
        else:
            return request.redirect("/portal/login")

    @http.route(["/portal/login"], type="http", auth="public", website=True)
    def registration_login(self, **kwargs):
        redirect_uri = request.params.get("redirect") or "/portal/home"
        if request.session and request.session.uid:
            return request.redirect(redirect_uri)

        context = {}

        if request.httprequest.method == "POST":
            res = Home().web_login(**kwargs)
            if request.params["login_success"]:
                return res
            else:
                context["error"] = "Invalid Credentials"

        return request.render("g2p_portal_base.login_page", qcontext=context)

    @http.route(["/portal/home"], type="http", auth="user", website=True)
    def portal_home(self, **kwargs):
        self.check_roles("Registration Portal User")
        return request.render("g2p_portal_base.home_page")

    @http.route(["/portal/myprofile"], type="http", auth="public", website=True)
    def portal_profile(self, **kwargs):
        if request.session and request.session.uid:
            current_partner = request.env.user.partner_id
            return request.render(
                "g2p_portal_base.profile_page",
                {
                    "current_partner": current_partner,
                },
            )

    @http.route(["/portal/aboutus"], type="http", auth="public", website=True)
    def portal_about_us(self, **kwargs):
        return request.render("g2p_portal_base.about_us_page")

    @http.route(["/portal/contactus"], type="http", auth="public", website=True)
    def portal_contact_us(self, **kwargs):
        return request.render("g2p_portal_base.contact_us_page")

    @http.route(["/portal/otherpage"], type="http", auth="public", website=True)
    def portal_other_page(self, **kwargs):
        return request.render("g2p_portal_base.other_page")

    def check_roles(self, role_to_check):
        if role_to_check == "Registration Portal User":
            if not request.session or not request.env.user:
                raise Unauthorized(_("User is not logged in"))
            if not request.env.user.partner_id.supplier_rank > 0:
                raise Forbidden(_AppendAction("User is not allowed to access the portal"))
