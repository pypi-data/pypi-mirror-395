this.ckan.module('search-through-content', function($) {
	return {
		options : {
                  target: null,
		},
		initialize: function () {
			$.proxyAll(this, /_on/);
            this.el.on("keyup", this._onSearch);
		},
        _onSearch: function() {
            var searchText = $(this.el).val().toLowerCase();
            $(this.options.target).each(function () {
                var text = $(this).text().toLowerCase();
                $(this).toggle(text.includes(searchText));
            });
        },
	};
});