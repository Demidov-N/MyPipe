    document.addEventListener('DOMContentLoaded', function() {
        var elem = document.querySelector('.sidenav');
        var collapsibleInstance = M.Sidenav.init(elem, {});
        var collapsibleElem = document.querySelector('.collapsible');
        var collapsibleInstance = M.Collapsible.init(collapsibleElem);
    });


    document.addEventListener('DOMContentLoaded', function() {
        var elems = document.querySelectorAll('.dropdown-trigger');
        var instances = M.Dropdown.init(elems, {
                hover: true,
                coverTrigger: false,
                constrainWidth: true
                });
            });
