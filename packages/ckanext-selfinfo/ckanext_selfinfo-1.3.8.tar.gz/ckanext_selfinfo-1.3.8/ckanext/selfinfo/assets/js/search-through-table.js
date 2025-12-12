ckan.module('search-through-table', function ($, _) {
    return {
        options : {
            targetTable: null,
        },
        initialize: function () {
            const input = this.el;
            const tableId = this.options.targetTable;
            const table = $('#' + tableId);
            const rows = table.find('tbody tr');
            input.on('input', function () {
                const filter = $(this).val().toLowerCase();
                rows.each(function () {
                const text = $(this).text().toLowerCase();
                $(this).toggle(text.includes(filter));
                });
            });
        }
    };
});
