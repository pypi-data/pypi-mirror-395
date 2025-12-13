#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：李锋
# @Software ：PyCharm
# @Date     ：2025/11/17 下午2:13
# @Desc     ：

from fastapi import Depends

from shudaodao_auth import AuthAPIRouter, AuthService
from shudaodao_auth.entity_table.t_auth_user import AuthUserResponse
from shudaodao_core import ResponseUtil
from ..package_config import PackageConfig
from ..schemas.menu_item import MenuItem

Acm_Controller = AuthAPIRouter(
    prefix=f"/v1/{PackageConfig.RouterPath}",
    tags=[f"{PackageConfig.RouterTags}"],
    db_engine_name=PackageConfig.EngineName,
)


# 受保护的路由
@Acm_Controller.get(
    "/system/menus", summary="获取当前用户的系统菜单",
    response_model=MenuItem
)
async def system_menus(
        current_user: AuthUserResponse = Depends(AuthService.get_current_user)
):
    menus_data = [
        {
            "name": "Dashboard",
            "path": "/dashboard",
            "component": "/index/index",
            "meta": {
                "title": "工作台",
                "icon": "ri:pie-chart-line"
            },
            "children": [
                {
                    "path": "console",
                    "name": "Console",
                    "component": "/dashboard/console",
                    "meta": {
                        "title": "欢迎页",
                        "icon": "ri:home-smile-2-line",
                        "keepAlive": True,
                        "fixedTab": True
                    }
                },
                {
                    "path": "analysis",
                    "name": "Analysis",
                    "component": "/dashboard/analysis",
                    "meta": {
                        "title": "分析页",
                        "icon": "ri:align-item-bottom-line",
                        "keepAlive": False
                    }
                },
                {
                    "path": "ecommerce",
                    "name": "Ecommerce",
                    "component": "/dashboard/ecommerce",
                    "meta": {
                        "title": "商务页",
                        "icon": "ri:bar-chart-box-line",
                        "keepAlive": False
                    }
                }
            ]
        },
        {
            "id": "11111111111",
            "path": "system",
            "name": "System",
            "component": "/index/index",
            "meta": {
                "title": "系统设置",
                "icon": "ri:user-3-line"
            },
            "children": [
                {
                    "id": "11111111111",
                    "path": "User",
                    "name": "User",
                    "component": "/shudaodao_acm/system",
                    "meta": {
                        "title": "模块(菜单)管理",
                        "icon": "ri:user-line",
                        "keepAlive": True,
                        "roles": [
                            "R_SUPER",
                            "R_ADMIN"
                        ]
                    }
                },
                {
                    "id": "11111111111",
                    "path": "role",
                    "name": "Role",
                    "component": "/shudaodao_acm/generate/table/sys_department",
                    "meta": {
                        "id": "11111111111",
                        "title": "部门(组织)管理",
                        "icon": "ri:user-settings-line",
                        "keepAlive": True,
                        "roles": [
                            "R_SUPER"
                        ]
                    }
                },
                {
                    "path": "user-center2",
                    "name": "UserCenter2",
                    "component": "/shudaodao_demo/table-form-compose",
                    "meta": {
                        "id": "22222222",
                        "title": "TableForm - 组装",
                        "icon": "ri:user-line",
                        "isHide": False,
                        "keepAlive": True,
                        "isHideTab": False
                    }
                },
                {
                    "path": "user-center1",
                    "name": "UserCenter1",
                    "component": "/shudaodao_demo/table-form",
                    "meta": {
                        "id": "11111111111",
                        "title": "TableForm - 标准",
                        "icon": "ri:user-line",
                        "isHide": False,
                        "keepAlive": True,
                        "isHideTab": False
                    }
                },
                {
                    "path": "menu",
                    "name": "Menus",
                    "component": "/system/menu",
                    "meta": {
                        "title": "menus.system.menu",
                        "icon": "ri:menu-line",
                        "keepAlive": True,
                        "roles": [
                            "R_SUPER"
                        ],
                        "authList": [
                            {
                                "title": "新增",
                                "authMark": "add"
                            },
                            {
                                "title": "编辑",
                                "authMark": "edit"
                            },
                            {
                                "title": "删除",
                                "authMark": "delete"
                            }
                        ]
                    }
                },
                {
                    "path": "nested",
                    "name": "Nested",
                    "component": "",
                    "meta": {
                        "title": "menus.system.nested",
                        "icon": "ri:menu-unfold-3-line",
                        "keepAlive": True
                    },
                    "children": [
                        {
                            "path": "menu1",
                            "name": "NestedMenu1",
                            "component": "/system/nested/menu1",
                            "meta": {
                                "title": "menus.system.menu1",
                                "icon": "ri:align-justify",
                                "keepAlive": True
                            }
                        },
                        {
                            "path": "menu2",
                            "name": "NestedMenu2",
                            "component": "",
                            "meta": {
                                "title": "menus.system.menu2",
                                "icon": "ri:align-justify",
                                "keepAlive": True
                            },
                            "children": [
                                {
                                    "path": "menu2-1",
                                    "name": "NestedMenu2-1",
                                    "component": "/system/nested/menu2",
                                    "meta": {
                                        "title": "menus.system.menu21",
                                        "icon": "ri:align-justify",
                                        "keepAlive": True
                                    }
                                }
                            ]
                        },
                        {
                            "path": "menu3",
                            "name": "NestedMenu3",
                            "component": "",
                            "meta": {
                                "title": "menus.system.menu3",
                                "icon": "ri:align-justify",
                                "keepAlive": True
                            },
                            "children": [
                                {
                                    "path": "menu3-1",
                                    "name": "NestedMenu3-1",
                                    "component": "/system/nested/menu3",
                                    "meta": {
                                        "title": "menus.system.menu31",
                                        "keepAlive": True
                                    }
                                },
                                {
                                    "path": "menu3-2",
                                    "name": "NestedMenu3-2",
                                    "component": "",
                                    "meta": {
                                        "title": "menus.system.menu32",
                                        "keepAlive": True
                                    },
                                    "children": [
                                        {
                                            "path": "menu3-2-1",
                                            "name": "NestedMenu3-2-1",
                                            "component": "/system/nested/menu3/menu3-2",
                                            "meta": {
                                                "title": "menus.system.menu321",
                                                "keepAlive": True
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "path": "/template",
            "name": "Template",
            "component": "/index/index",
            "meta": {
                "title": "模版中心",
                "icon": "ri:apps-2-line"
            },
            "children": [
                {
                    "path": "cards",
                    "name": "Cards",
                    "component": "/template/cards",
                    "meta": {
                        "title": "menus.template.cards",
                        "icon": "ri:wallet-line",
                        "keepAlive": False
                    }
                },
                {
                    "path": "banners",
                    "name": "Banners",
                    "component": "/template/banners",
                    "meta": {
                        "title": "menus.template.banners",
                        "icon": "ri:rectangle-line",
                        "keepAlive": False
                    }
                },
                {
                    "path": "charts",
                    "name": "Charts",
                    "component": "/template/charts",
                    "meta": {
                        "title": "menus.template.charts",
                        "icon": "ri:bar-chart-box-line",
                        "keepAlive": False
                    }
                },
                {
                    "path": "map",
                    "name": "Map",
                    "component": "/template/map",
                    "meta": {
                        "title": "menus.template.map",
                        "icon": "ri:map-pin-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "chat",
                    "name": "Chat",
                    "component": "/template/chat",
                    "meta": {
                        "title": "menus.template.chat",
                        "icon": "ri:message-3-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "calendar",
                    "name": "Calendar",
                    "component": "/template/calendar",
                    "meta": {
                        "title": "menus.template.calendar",
                        "icon": "ri:calendar-2-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "pricing",
                    "name": "Pricing",
                    "component": "/template/pricing",
                    "meta": {
                        "title": "menus.template.pricing",
                        "icon": "ri:money-cny-box-line",
                        "keepAlive": True,
                        "isFullPage": True
                    }
                }
            ]
        },
        {
            "path": "/widgets",
            "name": "Widgets",
            "component": "/index/index",
            "meta": {
                "title": "组件中心",
                "icon": "ri:apps-2-add-line"
            },
            "children": [
                {
                    "path": "icon",
                    "name": "Icon",
                    "component": "/widgets/icon",
                    "meta": {
                        "title": "menus.widgets.icon",
                        "icon": "ri:palette-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "image-crop",
                    "name": "ImageCrop",
                    "component": "/widgets/image-crop",
                    "meta": {
                        "title": "menus.widgets.imageCrop",
                        "icon": "ri:screenshot-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "excel",
                    "name": "Excel",
                    "component": "/widgets/excel",
                    "meta": {
                        "title": "menus.widgets.excel",
                        "icon": "ri:download-2-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "video",
                    "name": "Video",
                    "component": "/widgets/video",
                    "meta": {
                        "title": "menus.widgets.video",
                        "icon": "ri:vidicon-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "count-to",
                    "name": "CountTo",
                    "component": "/widgets/count-to",
                    "meta": {
                        "title": "menus.widgets.countTo",
                        "icon": "ri:anthropic-line",
                        "keepAlive": False
                    }
                },
                {
                    "path": "wang-editor",
                    "name": "WangEditor",
                    "component": "/widgets/wang-editor",
                    "meta": {
                        "title": "menus.widgets.wangEditor",
                        "icon": "ri:t-box-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "watermark",
                    "name": "Watermark",
                    "component": "/widgets/watermark",
                    "meta": {
                        "title": "menus.widgets.watermark",
                        "icon": "ri:water-flash-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "context-menu",
                    "name": "ContextMenu",
                    "component": "/widgets/context-menu",
                    "meta": {
                        "title": "menus.widgets.contextMenu",
                        "icon": "ri:menu-2-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "qrcode",
                    "name": "Qrcode",
                    "component": "/widgets/qrcode",
                    "meta": {
                        "title": "menus.widgets.qrcode",
                        "icon": "ri:qr-code-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "drag",
                    "name": "Drag",
                    "component": "/widgets/drag",
                    "meta": {
                        "title": "menus.widgets.drag",
                        "icon": "ri:drag-move-fill",
                        "keepAlive": True
                    }
                },
                {
                    "path": "text-scroll",
                    "name": "TextScroll",
                    "component": "/widgets/text-scroll",
                    "meta": {
                        "title": "menus.widgets.textScroll",
                        "icon": "ri:input-method-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "fireworks",
                    "name": "Fireworks",
                    "component": "/widgets/fireworks",
                    "meta": {
                        "title": "menus.widgets.fireworks",
                        "icon": "ri:magic-line",
                        "keepAlive": True,
                        "showTextBadge": "Hot"
                    }
                },
                {
                    "path": "/outside/iframe/elementui",
                    "name": "ElementUI",
                    "component": "",
                    "meta": {
                        "title": "menus.widgets.elementUI",
                        "icon": "ri:apps-2-line",
                        "keepAlive": False,
                        "link": "https://element-plus.org/zh-CN/component/overview.html",
                        "isIframe": True
                    }
                }
            ]
        },
        {
            "path": "/examples",
            "name": "Examples",
            "component": "/index/index",
            "meta": {
                "title": "功能示例",
                "icon": "ri:sparkling-line"
            },
            "children": [
                {
                    "path": "permission",
                    "name": "Permission",
                    "component": "",
                    "meta": {
                        "title": "menus.examples.permission.title",
                        "icon": "ri:fingerprint-line"
                    },
                    "children": [
                        {
                            "path": "switch-role",
                            "name": "PermissionSwitchRole",
                            "component": "/examples/permission/switch-role",
                            "meta": {
                                "title": "menus.examples.permission.switchRole",
                                "icon": "ri:contacts-line",
                                "keepAlive": True
                            }
                        },
                        {
                            "path": "button-auth",
                            "name": "PermissionButtonAuth",
                            "component": "/examples/permission/button-auth",
                            "meta": {
                                "title": "menus.examples.permission.buttonAuth",
                                "icon": "ri:mouse-line",
                                "keepAlive": True,
                                "authList": [
                                    {
                                        "title": "新增",
                                        "authMark": "add"
                                    },
                                    {
                                        "title": "编辑",
                                        "authMark": "edit"
                                    },
                                    {
                                        "title": "删除",
                                        "authMark": "delete"
                                    },
                                    {
                                        "title": "导出",
                                        "authMark": "export"
                                    },
                                    {
                                        "title": "查看",
                                        "authMark": "view"
                                    },
                                    {
                                        "title": "发布",
                                        "authMark": "publish"
                                    },
                                    {
                                        "title": "配置",
                                        "authMark": "config"
                                    },
                                    {
                                        "title": "管理",
                                        "authMark": "manage"
                                    }
                                ]
                            }
                        },
                        {
                            "path": "page-visibility",
                            "name": "PermissionPageVisibility",
                            "component": "/examples/permission/page-visibility",
                            "meta": {
                                "title": "menus.examples.permission.pageVisibility",
                                "icon": "ri:user-3-line",
                                "keepAlive": True,
                                "roles": [
                                    "R_SUPER"
                                ]
                            }
                        }
                    ]
                },
                {
                    "path": "tabs",
                    "name": "Tabs",
                    "component": "/examples/tabs",
                    "meta": {
                        "title": "menus.examples.tabs",
                        "icon": "ri:price-tag-line"
                    }
                },
                {
                    "path": "tables/basic",
                    "name": "TablesBasic",
                    "component": "/examples/tables/basic",
                    "meta": {
                        "title": "menus.examples.tablesBasic",
                        "icon": "ri:layout-grid-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "tables",
                    "name": "Tables",
                    "component": "/examples/tables",
                    "meta": {
                        "title": "menus.examples.tables",
                        "icon": "ri:table-3",
                        "keepAlive": True
                    }
                },
                {
                    "path": "forms",
                    "name": "Forms",
                    "component": "/examples/forms",
                    "meta": {
                        "title": "menus.examples.forms",
                        "icon": "ri:table-view",
                        "keepAlive": True
                    }
                },
                {
                    "path": "form/search-bar",
                    "name": "SearchBar",
                    "component": "/examples/forms/search-bar",
                    "meta": {
                        "title": "menus.examples.searchBar",
                        "icon": "ri:table-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "tables/tree",
                    "name": "TablesTree",
                    "component": "/examples/tables/tree",
                    "meta": {
                        "title": "menus.examples.tablesTree",
                        "icon": "ri:layout-2-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "socket-chat",
                    "name": "SocketChat",
                    "component": "/examples/socket-chat",
                    "meta": {
                        "title": "menus.examples.socketChat",
                        "icon": "ri:shake-hands-line",
                        "keepAlive": True,
                        "showTextBadge": "New"
                    }
                }
            ]
        },

        {
            "path": "/article",
            "name": "Article",
            "component": "/index/index",
            "meta": {
                "title": "文章管理",
                "icon": "ri:book-2-line"
            },
            "children": [
                {
                    "path": "article-list",
                    "name": "ArticleList",
                    "component": "/article/list",
                    "meta": {
                        "title": "menus.article.articleList",
                        "icon": "ri:article-line",
                        "keepAlive": True,
                        "authList": [
                            {
                                "title": "新增",
                                "authMark": "add"
                            },
                            {
                                "title": "编辑",
                                "authMark": "edit"
                            }
                        ]
                    }
                },
                {
                    "path": "detail/:id",
                    "name": "ArticleDetail",
                    "component": "/article/detail",
                    "meta": {
                        "title": "menus.article.articleDetail",
                        "isHide": True,
                        "keepAlive": True,
                        "activePath": "/article/article-list"
                    }
                },
                {
                    "path": "comment",
                    "name": "ArticleComment",
                    "component": "/article/comment",
                    "meta": {
                        "title": "menus.article.comment",
                        "icon": "ri:mail-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "publish",
                    "name": "ArticlePublish",
                    "component": "/article/publish",
                    "meta": {
                        "title": "menus.article.articlePublish",
                        "icon": "ri:telegram-2-line",
                        "keepAlive": True,
                        "authList": [
                            {
                                "title": "发布",
                                "authMark": "add"
                            }
                        ]
                    }
                }
            ]
        },
        {
            "path": "/result",
            "name": "Result",
            "component": "/index/index",
            "meta": {
                "title": "系统页面",
                "icon": "ri:checkbox-circle-line"
            },
            "children": [
                {
                    "path": "success",
                    "name": "ResultSuccess",
                    "component": "/result/success",
                    "meta": {
                        "title": "成功页",
                        "icon": "ri:checkbox-circle-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "fail",
                    "name": "ResultFail",
                    "component": "/result/fail",
                    "meta": {
                        "title": "失败",
                        "icon": "ri:close-circle-line",
                        "keepAlive": True
                    }
                },
                {
                    "path": "403",
                    "name": "403",
                    "component": "/exception/403",
                    "meta": {
                        "title": "错误页-403",
                        "icon": "ri:close-circle-line",
                        "keepAlive": True,
                        "isFullPage": False
                    }
                },
                {
                    "path": "404",
                    "name": "404",
                    "component": "/exception/404",
                    "meta": {
                        "title": "错误页-404",
                        "icon": "ri:close-circle-line",
                        "keepAlive": True,
                        "isFullPage": False
                    }
                },
                {
                    "path": "500",
                    "name": "500",
                    "component": "/exception/500",
                    "meta": {
                        "title": "错误页-500",
                        "icon": "ri:close-circle-line",
                        "keepAlive": True,
                        "isFullPage": False
                    }
                }
            ]
        },
        {
            "path": "/safeguard",
            "name": "Safeguard",
            "component": "/index/index",
            "meta": {
                "title": "menus.safeguard.title",
                "icon": "ri:shield-check-line",
                "keepAlive": False
            },
            "children": [
                {
                    "path": "server",
                    "name": "SafeguardServer",
                    "component": "/safeguard/server",
                    "meta": {
                        "title": "menus.safeguard.server",
                        "icon": "ri:hard-drive-3-line",
                        "keepAlive": True
                    }
                }
            ]
        },
        # {
        #     "name": "Document",
        #     "path": "",
        #     "component": "",
        #     "meta": {
        #         "title": "menus.help.document",
        #         "icon": "ri:bill-line",
        #         "link": "https://www.artd.pro/docs/zh/",
        #         "isIframe": False,
        #         "keepAlive": False,
        #         "isFirstLevel": True
        #     }
        # },
        # {
        #     "name": "LiteVersion",
        #     "path": "",
        #     "component": "",
        #     "meta": {
        #         "title": "menus.help.liteVersion",
        #         "icon": "ri:bus-2-line",
        #         "link": "https://www.artd.pro/docs/zh/guide/lite-version.html",
        #         "isIframe": False,
        #         "keepAlive": False,
        #         "isFirstLevel": True
        #     }
        # },
        # {
        #     "name": "ChangeLog",
        #     "path": "/change/log",
        #     "component": "/change/log",
        #     "meta": {
        #         "title": "menus.plan.log",
        #         "icon": "ri:gamepad-line",
        #         "keepAlive": False,
        #         "isFirstLevel": True
        #     }
        # }
    ]
    return ResponseUtil.success(
        message="获取当前用户的系统菜单成功",
        data=menus_data
    )
