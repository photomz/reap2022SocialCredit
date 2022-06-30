(window["webpackJsonp"] = window["webpackJsonp"] || []).push([
  ["chunk-2d224582"],
  {
    e078: function (t, e, n) {
      "use strict";
      n.r(e);
      var o = function () {
          var t = this,
            e = t.$createElement,
            n = t._self._c || e;
          return n(
            "div",
            {
              staticClass: "head",
              staticStyle: {
                width: "143px",
                position: "relative",
                height: "117px",
              },
              attrs: { id: "loginm" },
            },
            [
              n(
                "div",
                {
                  staticStyle: {
                    position: "absolute",
                    top: "0",
                    right: "0",
                    height: "100%",
                    "font-size": "14px",
                    "z-index": "9999999999",
                  },
                },
                [
                  t.isShowRegister
                    ? n(
                        "Dropdown",
                        {
                          staticStyle: { "margin-left": "10px" },
                          scopedSlots: t._u(
                            [
                              {
                                key: "list",
                                fn: function () {
                                  return [
                                    n(
                                      "DropdownMenu",
                                      [
                                        n(
                                          "DropdownItem",
                                          {
                                            nativeOn: {
                                              click: function (e) {
                                                return t.linkToRegistrationPer.apply(
                                                  null,
                                                  arguments
                                                );
                                              },
                                            },
                                          },
                                          [t._v("个人注册")]
                                        ),
                                        n(
                                          "DropdownItem",
                                          {
                                            nativeOn: {
                                              click: function (e) {
                                                return t.linkToRegistrationLep.apply(
                                                  null,
                                                  arguments
                                                );
                                              },
                                            },
                                          },
                                          [t._v("法人注册")]
                                        ),
                                      ],
                                      1
                                    ),
                                  ];
                                },
                                proxy: !0,
                              },
                            ],
                            null,
                            !1,
                            3756884760
                          ),
                        },
                        [n("Button", [t._v(" 注册 ")])],
                        1
                      )
                    : t._e(),
                  t.token
                    ? n(
                        "a",
                        {
                          staticStyle: { padding: "10px 5px" },
                          attrs: { href: "javascript:;" },
                          on: { click: t.linkToCenter },
                        },
                        [t._v(t._s(t.userName))]
                      )
                    : n(
                        "Dropdown",
                        {
                          staticStyle: { "margin-left": "10px" },
                          scopedSlots: t._u(
                            [
                              {
                                key: "list",
                                fn: function () {
                                  return [
                                    n(
                                      "DropdownMenu",
                                      [
                                        n(
                                          "DropdownItem",
                                          {
                                            nativeOn: {
                                              click: function (e) {
                                                return t.linkToLoginPer.apply(
                                                  null,
                                                  arguments
                                                );
                                              },
                                            },
                                          },
                                          [t._v("个人登录")]
                                        ),
                                        n(
                                          "DropdownItem",
                                          {
                                            nativeOn: {
                                              click: function (e) {
                                                return t.linkToLoginLep.apply(
                                                  null,
                                                  arguments
                                                );
                                              },
                                            },
                                          },
                                          [t._v("法人登录")]
                                        ),
                                      ],
                                      1
                                    ),
                                  ];
                                },
                                proxy: !0,
                              },
                            ],
                            null,
                            !1,
                            3824684856
                          ),
                        },
                        [
                          n("Button", { attrs: { type: "primary" } }, [
                            t._v(" 登录 "),
                          ]),
                        ],
                        1
                      ),
                  t.token
                    ? n("a", { attrs: { href: "javascript:;" } }, [
                        t._v("         "),
                      ])
                    : t._e(),
                ],
                1
              ),
            ]
          );
        },
        a = [],
        s = (n("765a"), n("9fd3"), n("141e"), n("7701"), n("365c")),
        i = n("fa7d"),
        r = {
          name: "shead",
          data: function () {
            return { isShowRegister: !0, token: "", flag: "", userName: "" };
          },
          created: function () {
            location.href.indexOf("zwfwUser=1") > -1 &&
              (location.href =
                "https://puser.zjzwfw.gov.cn/sso/newusp.do?action=ssoLogin&servicecode=sggxyxxpt&goto=" +
                this._$Url1),
              location.href.indexOf("zwfwUser=2") > -1 &&
                (location.href =
                  "https://esso.zjzwfw.gov.cn/opensso/spsaehandler/metaAlias/sp?spappurl=https://creditydd.fzggw.zj.gov.cn/ding/sign/signController/obtainLegalPersonSsotoken?goto=" +
                  this._$Url2);
          },
          mounted: function () {
            this.initUser();
          },
          methods: {
            initUser: function () {
              var t = this;
              i["a"].getQueryString("token")
                ? ((this.token = i["a"].getQueryString("token") || ""),
                  (this.flag = i["a"].getQueryString("flag").slice(0, 1) || ""))
                : ((this.token = ""), (this.flag = "")),
                s["a"]
                  ._creditZlbGetUserInfo({
                    flag: this.flag || "",
                    token: this.token || "",
                  })
                  .then(function (e) {
                    if (e.data.success) {
                      e.data.data && e.data.data.certName
                        ? (t.isShowRegister = !1)
                        : (t.isShowRegister = !0),
                        (t.userName = e.data.data && e.data.data.realName);
                      var n = e.data.data && e.data.data.certNo;
                      sessionStorage.setItem("name", t.userName || ""),
                        sessionStorage.setItem("realName", t.userName || ""),
                        sessionStorage.setItem("code", n || ""),
                        sessionStorage.getItem("attnName") ||
                          sessionStorage.setItem(
                            "attnName",
                            e.data.data && e.data.data.linkPerson
                              ? e.data.data.linkPerson
                              : ""
                          ),
                        sessionStorage.getItem("attnPhone") ||
                          sessionStorage.setItem(
                            "attnPhone",
                            e.data.data && e.data.data.linkPhone
                              ? e.data.data && e.data.data.linkPhone
                              : ""
                          ),
                        location.search.indexOf("admin=1") > -1 &&
                          t.$router.push("/userCenter/creditObjection"),
                        location.search.indexOf("grda=") > -1 &&
                          t.$router.push("/userCenter/creditFile");
                    }
                  });
            },
            linkToRegistrationPer: function () {
              window.open(
                "https://puser.zjzwfw.gov.cn/sso/usp.do?action=register&servicecode=njdh",
                "_blank"
              );
            },
            linkToRegistrationLep: function () {
              window.open(
                "https://uuser.zjzwfw.gov.cn/jsp/client/uuuser/uuuserRegistStep1.jsp?",
                "_blank"
              );
            },
            linkToLoginPer: function () {
              window.open(
                "https://puser.zjzwfw.gov.cn/sso/newusp.do?action=ssoLogin&servicecode=sggxyxxpt&goto=" +
                  this.$Url,
                "_blank"
              );
            },
            linkToLoginLep: function () {
              window.open(
                "https://esso.zjzwfw.gov.cn/opensso/spsaehandler/metaAlias/sp?spappurl=https://creditydd.fzggw.zj.gov.cn/ding/sign/signController/obtainLegalPersonSsotoken?goto=" +
                  this.$UserCenterUrl,
                "_blank"
              );
            },
            linkToCenter: function () {
              window.open(
                "https://xyxx.zjzwfw.gov.cn/jyh1/?token="
                  .concat(this.token, "&flag=")
                  .concat(this.flag, "/#/userCenter/creditFile"),
                "_blank"
              );
            },
          },
          watch: {},
        },
        l = r,
        c = n("cba8"),
        d = Object(c["a"])(l, o, a, !1, null, null, null);
      e["default"] = d.exports;
    },
  },
]);
