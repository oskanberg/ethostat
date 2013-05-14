

function thermometer = {
    this.
}

$(document).ready(function()
{
    console.log("hello!");
    var temperatureAPI = "http://127.0.0.1:5000/query?callback=?";
    console.log(temperatureAPI);
    $.getJSON( temperatureAPI,
    {
        keyword: "hello",
    })
    .done(function(data) {
        var items = [];
        $.each(data, function(key, val)
        {
            items.push('<p>term: ' + key + '<br />temp: ' + val + '</p>');
        });
        $('<ul/>',
            {
                'class': 'my-new-list',
                html: items.join('')
            }
        )
        .appendTo('body');
    });
});

