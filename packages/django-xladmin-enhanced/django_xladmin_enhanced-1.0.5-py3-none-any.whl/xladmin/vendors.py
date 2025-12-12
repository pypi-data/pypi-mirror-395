
vendors = {
    "bootstrap": {
        'js': {
            'dev': 'xladmin/vendor/bootstrap/js/bootstrap.js',
            'production': 'xladmin/vendor/bootstrap/js/bootstrap.min.js',
            'cdn': 'http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js'
        },
        'css': {
            'dev': 'xladmin/vendor/bootstrap/css/bootstrap.css',
            'production': 'xladmin/vendor/bootstrap/css/bootstrap.css',
            'cdn': 'http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css'
        },
        'responsive': {'css':{
                'dev': 'xladmin/vendor/bootstrap/bootstrap-responsive.css',
                'production': 'xladmin/vendor/bootstrap/bootstrap-responsive.css'
            }}
    },
    'jquery': {
        "js": {
            'dev': 'xladmin/vendor/jquery/jquery.js',
            'production': 'xladmin/vendor/jquery/jquery.min.js',
        }
    },
    'jquery-ui-effect': {
        "js": {
            'dev': 'xladmin/vendor/jquery-ui/jquery.ui.effect.js',
            'production': 'xladmin/vendor/jquery-ui/jquery.ui.effect.min.js'
        }
    },
    'jquery-ui-sortable': {
        "js": {
            'dev': ['xladmin/vendor/jquery-ui/jquery.ui.core.js', 'xladmin/vendor/jquery-ui/jquery.ui.widget.js',
                    'xladmin/vendor/jquery-ui/jquery.ui.mouse.js', 'xladmin/vendor/jquery-ui/jquery.ui.sortable.js'],
            'production': ['xladmin/vendor/jquery-ui/jquery.ui.core.min.js', 'xladmin/vendor/jquery-ui/jquery.ui.widget.min.js',
                           'xladmin/vendor/jquery-ui/jquery.ui.mouse.min.js', 'xladmin/vendor/jquery-ui/jquery.ui.sortable.min.js']
        }
    },
    "font-awesome": {
        "css": {
            'dev': 'xladmin/vendor/font-awesome/css/font-awesome.css',
            'production': 'xladmin/vendor/font-awesome/css/font-awesome.min.css',
        }
    },
    "timepicker": {
        "css": {
            'dev': 'xladmin/vendor/bootstrap-timepicker/css/bootstrap-timepicker.css',
            'production': 'xladmin/vendor/bootstrap-timepicker/css/bootstrap-timepicker.min.css',
        },
        "js": {
            'dev': 'xladmin/vendor/bootstrap-timepicker/js/bootstrap-timepicker.js',
            'production': 'xladmin/vendor/bootstrap-timepicker/js/bootstrap-timepicker.min.js',
        }
    },
    "clockpicker": {
        "css": {
            'dev': 'xladmin/vendor/bootstrap-clockpicker/bootstrap-clockpicker.css',
            'production': 'xladmin/vendor/bootstrap-clockpicker/bootstrap-clockpicker.min.css',
        },
        "js": {
            'dev': 'xladmin/vendor/bootstrap-clockpicker/bootstrap-clockpicker.js',
            'production': 'xladmin/vendor/bootstrap-clockpicker/bootstrap-clockpicker.min.js',
        }
    },
    "datepicker": {
        "css": {
            'dev': 'xladmin/vendor/bootstrap-datepicker/css/datepicker.css'
        },
        "js": {
            'dev': 'xladmin/vendor/bootstrap-datepicker/js/bootstrap-datepicker.js',
        }
    },
    "flot": {
        "js": {
            'dev': ['xladmin/vendor/flot/jquery.flot.js', 'xladmin/vendor/flot/jquery.flot.pie.js', 'xladmin/vendor/flot/jquery.flot.time.js',
                    'xladmin/vendor/flot/jquery.flot.resize.js','xladmin/vendor/flot/jquery.flot.aggregate.js','xladmin/vendor/flot/jquery.flot.categories.js']
        }
    },
    "image-gallery": {
        "css": {
            'dev': 'xladmin/vendor/bootstrap-image-gallery/css/bootstrap-image-gallery.css',
            'production': 'xladmin/vendor/bootstrap-image-gallery/css/bootstrap-image-gallery.css',
        },
        "js": {
            'dev': ['xladmin/vendor/load-image/load-image.js', 'xladmin/vendor/bootstrap-image-gallery/js/bootstrap-image-gallery.js'],
            'production': ['xladmin/vendor/load-image/load-image.min.js', 'xladmin/vendor/bootstrap-image-gallery/js/bootstrap-image-gallery.js']
        }
    },
    "select": {
        "css": {
            'dev': ['xladmin/vendor/select2/select2.css', 'xladmin/vendor/selectize/selectize.css', 'xladmin/vendor/selectize/selectize.bootstrap3.css'],
        },
        "js": {
            'dev': ['xladmin/vendor/selectize/selectize.js', 'xladmin/vendor/select2/select2.js', 'xladmin/vendor/select2/select2_locale_%(lang)s.js'],
            'production': ['xladmin/vendor/selectize/selectize.min.js', 'xladmin/vendor/select2/select2.min.js', 'xladmin/vendor/select2/select2_locale_%(lang)s.js']
        }
    },
    "multiselect": {
        "css": {
            'dev': 'xladmin/vendor/bootstrap-multiselect/css/bootstrap-multiselect.css',
        },
        "js": {
            'dev': 'xladmin/vendor/bootstrap-multiselect/js/bootstrap-multiselect.js',
        }
    },
    "snapjs": {
        "css": {
            'dev': 'xladmin/vendor/snapjs/snap.css',
        },
        "js": {
            'dev': 'xladmin/vendor/snapjs/snap.js',
        }
    },
    # XLAdmin specific files
    "xladmin": {
        "js": {
            'dev': 'xladmin/js/',
        },
        "css": {
            'dev': 'xladmin/css/',
        }
    },
    # XLAdmin plugin files
    "xladmin.plugin.themes": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.themes.js',
        }
    },
    "xladmin.plugin.portal": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.portal.js',
        }
    },
    "xladmin.plugin.details": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.details.js',
        }
    },
    "xladmin.plugin.sortablelist": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.sortablelist.js',
        }
    },
    "xladmin.plugin.charts": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.charts.js',
        }
    },
    "xladmin.plugin.actions": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.actions.js',
        }
    },
    "xladmin.plugin.bookmark": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.bookmark.js',
        }
    },
    "xladmin.plugin.importexport": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.importexport.js',
        },
        "css": {
            'dev': 'xladmin/css/xladmin.plugin.importexport.css',
        }
    },
    "xladmin.plugin.filters": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.filters.js',
        }
    },
    "xladmin.plugin.quickfilter": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.quickfilter.js',
        },
        "css": {
            'dev': 'xladmin/css/xladmin.plugin.quickfilter.css',
        }
    },
    "xladmin.plugin.revision": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.revision.js',
        }
    },
    "xladmin.plugin.refresh": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.refresh.js',
        }
    },
    "xladmin.plugin.quick-form": {
        "js": {
            'dev': 'xladmin/js/xladmin.plugin.quick-form.js',
        }
    },
    # XLAdmin page files
    "xladmin.page.form": {
        "js": {
            'dev': 'xladmin/js/xladmin.page.form.js',
        }
    },
    "xladmin.page.list": {
        "js": {
            'dev': 'xladmin/js/xladmin.page.list.js',
        }
    },
    "xladmin.page.dashboard": {
        "js": {
            'dev': 'xladmin/js/xladmin.page.dashboard.js',
        },
        "css": {
            'dev': 'xladmin/css/xladmin.page.dashboard.css',
        }
    },
    # XLAdmin form and plugin CSS
    "xladmin.form": {
        "css": {
            'dev': 'xladmin/css/xladmin.form.css',
        }
    },
    "xladmin.plugins": {
        "css": {
            'dev': 'xladmin/css/xladmin.plugins.css',
        }
    },
    "xladmin.mobile": {
        "css": {
            'dev': 'xladmin/css/xladmin.mobile.css',
        }
    },
    "xladmin.main": {
        "css": {
            'dev': 'xladmin/css/xladmin.main.css',
        },
        "js": {
            'dev': 'xladmin/js/xladmin.main.js',
        }
    },
    "xladmin.responsive": {
        "css": {
            'dev': 'xladmin/css/xladmin.responsive.css',
        },
        "js": {
            'dev': 'xladmin/js/xladmin.responsive.js',
        }
    },
    # Main XLAdmin files mapping
    'xladmin.main.css': 'xladmin/css/xladmin.main.css',
    'xladmin.plugins.css': 'xladmin/css/xladmin.plugins.css', 
    'xladmin.responsive.css': 'xladmin/css/xladmin.responsive.css',
    'xladmin.main.js': 'xladmin/js/xladmin.main.js',
    'xladmin.responsive.js': 'xladmin/js/xladmin.responsive.js',
}
