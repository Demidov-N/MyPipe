

    document.addEventListener('DOMContentLoaded', function() {
        var elem = document.querySelector('.sidenav');
        var collapsibleInstance = M.Sidenav.init(elem, {});
        var collapsibleElem = document.querySelector('.collapsible');
        var collapsibleInstance = M.Collapsible.init(collapsibleElem);
        var dropdown = document.querySelectorAll('.dropdown-trigger');
        var tabs = document.getElementById('tabs');
        var tab_init = M.Tabs.init(tabs, {});
        var instances = M.Dropdown.init(dropdown, {
                hover: true,
                coverTrigger: false,
                constrainWidth: true
                });
            });
