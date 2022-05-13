let cx, cy;
let gscale;
let fdata;
let pathdata;
let colorscheme;

function setup()
{
    createCanvas(1200, 900);
    cx = width / 2;
    cy = height / 2;
    gscale = 2;
    fdata = {
        'metadata': {
            'table_width': 200,
            'table_height': 400,
            'ball_radius': 7,
            'pocket_radius': 10,
            'railing_width': 30,
        },
        'balls':
        {
            '0': [0, 0],
            '1': [-20, 70],
            '12': [0, 50],
            '3': [-80, 80],
            '14': [20, 40],
            '9': [-20, 40],
        },
    };
    let tmp_bdist = fdata['metadata']['pocket_radius'] * (1 / 1.414);
    fdata['pockets'] = [
        [-(fdata['metadata']['table_width'] / 2) - tmp_bdist,  (fdata['metadata']['table_height'] / 2) + tmp_bdist],
        [ (fdata['metadata']['table_width'] / 2) + tmp_bdist,  (fdata['metadata']['table_height'] / 2) + tmp_bdist],
        [ (fdata['metadata']['table_width'] / 2) + tmp_bdist, -(fdata['metadata']['table_height'] / 2) - tmp_bdist],
        [-(fdata['metadata']['table_width'] / 2) - tmp_bdist, -(fdata['metadata']['table_height'] / 2) - tmp_bdist],
        [0,  (fdata['metadata']['table_height'] / 2) + fdata['metadata']['pocket_radius']],
        [0, -(fdata['metadata']['table_height'] / 2) - fdata['metadata']['pocket_radius']],
        [ (fdata['metadata']['table_width'] / 2) + fdata['metadata']['pocket_radius'], 0],
        [-(fdata['metadata']['table_width'] / 2) - fdata['metadata']['pocket_radius'], 0],
    ];
    colorscheme = {
        'table_cloth': color(14, 204, 65),
        'table_wood': color(127, 87, 22),
        'ball': {
            '0': 'white',
            '1': 'yellow',
            '2': 'blue',
            '3': 'red',
            '4': 'purple',
            '5': 'darkorange',
            '6': 'darkgreen',
            '7': 'maroon',
            '8': 'black',
        },
        'line': [
            'red',
            'blue',
            'black',
            'purple',
            'white',
        ],
    };
    pathdata = [];
    postData('/getpaths', {'frame_data': fdata})
        .then((resp) => {
            pathdata = resp['paths'];
        });
}

function draw()
{
    background(200);
    translate(cx, cy);

    // drawing the table
    noStroke();
    fill(colorscheme['table_wood']);
    srect(-(fdata['metadata']['table_width'] / 2) - fdata['metadata']['railing_width'], -(fdata['metadata']['table_height'] / 2) - fdata['metadata']['railing_width'], fdata['metadata']['table_width'] + 2 * fdata['metadata']['railing_width'], fdata['metadata']['table_height'] + 2 * fdata['metadata']['railing_width']);
    fill(colorscheme['table_cloth']);
    srect(-(fdata['metadata']['table_width'] / 2), -(fdata['metadata']['table_height'] / 2), fdata['metadata']['table_width'], fdata['metadata']['table_height']);

    // drawing the pockets
    fill('black');
    fdata['pockets'].forEach((pocket) =>
        {
            scircle(pocket[0], pocket[1], 2 * fdata['metadata']['pocket_radius']);
        });

    // drawing the paths
    strokeWeight(gscale);
    noFill();
    pathdata.forEach((path) =>
        {
            stroke(getRandomColor());
            path.forEach((line) =>
                {
                    sline(line[0], -line[1], line[2], -line[3]);
                }
            );
        }
    );

    // drawing the balls
    textAlign(CENTER, CENTER);
    textSize(gscale * 6);
    for(var ball in fdata['balls'])
    {
        noStroke();
        let cbx = fdata['balls'][ball][0];
        let cby = fdata['balls'][ball][1];
        let cbr = fdata['metadata']['ball_radius'];

        // primary color
        let pri_col;
        if(int(ball) > 8)
            pri_col = colorscheme['ball'][str(int(ball) - 8)];
        else
            pri_col = colorscheme['ball'][ball];
        // drawing the main circle
        fill(pri_col);
        scircle(cbx, -cby, 2 * cbr);

        // secondary color (centre and stripes)
        // text color
        let sec_col = 'white';
        let text_col = 'black';
        // 9 ball has opposite scheme
        if(ball == '9')
        {
            sec_col = 'black';
            text_col = 'white';
        }

        // draw a red dot for cue
        if(ball == '0')
        {
            fill('red');
            scircle(cbx, -cby, cbr / 2);
        }
        // if not cue then draw centre, stripes and text
        else
        {
            // drawing the stripes if the ball is more than 8
            if(int(ball) > 8)
            {
                fill(sec_col);
                sarc(cbx, -cby, 2 * cbr, 2 * cbr, -(HALF_PI / 2), (HALF_PI / 2));
                sarc(cbx, -cby, 2 * cbr, 2 * cbr, -(HALF_PI / 2) + PI, (HALF_PI / 2) + PI);
            }

            // drawing the centre circle to hold text
            fill(sec_col);
            scircle(cbx, -cby, 1.1 * cbr);

            // drawing the text
            fill(text_col);
            strokeWeight(0.5);
            stroke(text_col);
            stext(ball, cbx, -cby);
        }
    }

    // stopping the loop after receiving data
    if(pathdata.length > 0)
        noLoop();
}

function getRandomColor()
{
    let ind = int(Math.random() * colorscheme['line'].length);
    return colorscheme['line'][ind];
}

function sline(x1, y1, x2, y2)
{
    line(x1 * gscale, y1 * gscale, x2 * gscale, y2 * gscale);
}

function srect(x, y, wid, hei)
{
    rect(x * gscale, y * gscale, wid * gscale, hei * gscale);
}

function scircle(x, y, dia)
{
    circle(x * gscale, y * gscale, dia * gscale);
}

function stext(strtext, x, y)
{
    text(strtext, x * gscale, y * gscale);
}

function sarc(x, y, w, h, start, stop)
{
    arc(x * gscale, y * gscale, w * gscale, h * gscale, start, stop, CHORD);
}
