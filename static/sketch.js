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
    gscale = 1.8;
    fdata = {
        'metadata': {
            'table_width': 200,
            'table_height': 400,
            'ball_radius': 7,
            'pocket_radius': 9,
            'railing_width': 28,
            'grail_width': 9 * (1 / 1.414), // green railing
        },
        'balls':
        {
            '0': [0, 0],
            '1': [-20, 70],
            '12': [0, 50],
            '3': [-80, 80],
            '14': [40, 40],
            '9': [-20, 40],
        },
    };
    let tmp_bdist = fdata['metadata']['pocket_radius'] * 0.7;
    let tmp_bdist_ed = fdata['metadata']['pocket_radius'] * 1.4;
    fdata['pockets'] = [
        [-(fdata['metadata']['table_width'] / 2) - tmp_bdist,  (fdata['metadata']['table_height'] / 2) + tmp_bdist],
        [ (fdata['metadata']['table_width'] / 2) + tmp_bdist,  (fdata['metadata']['table_height'] / 2) + tmp_bdist],
        [ (fdata['metadata']['table_width'] / 2) + tmp_bdist, -(fdata['metadata']['table_height'] / 2) - tmp_bdist],
        [-(fdata['metadata']['table_width'] / 2) - tmp_bdist, -(fdata['metadata']['table_height'] / 2) - tmp_bdist],
        [ (fdata['metadata']['table_width'] / 2) + tmp_bdist_ed, 0],
        [-(fdata['metadata']['table_width'] / 2) - tmp_bdist_ed, 0],
    ];
    fdata['pockets_bound'] = [
        [1 * PI / 2, 4 * PI / 2],
        [2 * PI / 2, 1 * PI / 2],
        [3 * PI / 2, 2 * PI / 2],
        [0 * PI / 2, 3 * PI / 2],
        [2 * PI - (PI / 2) * 1.3, (PI / 2) * 1.3],
        [(PI / 2) * 0.7, 2 * PI - (PI / 2) * 0.7],
    ];
    let tmp_tri_sha = [
        fdata['pockets'][0][0],
        fdata['pockets'][0][1] - fdata['metadata']['pocket_radius'],
        fdata['pockets'][0][0] + fdata['metadata']['pocket_radius'],
        fdata['pockets'][0][1],
        fdata['pockets'][0][0] + 2.3 * fdata['metadata']['pocket_radius'],
        fdata['pockets'][0][1] - 1 * fdata['metadata']['pocket_radius'],
        fdata['pockets'][0][0] + 1 * fdata['metadata']['pocket_radius'],
        fdata['pockets'][0][1] - 2.3 * fdata['metadata']['pocket_radius'],
    ];
    fdata['shade_points'] = [
        [-(fdata['metadata']['table_width'] / 2) - fdata['metadata']['grail_width'], fdata['metadata']['pocket_radius'], fdata['metadata']['grail_width'], 2 * fdata['metadata']['pocket_radius']],
        [ (fdata['metadata']['table_width'] / 2), fdata['metadata']['pocket_radius'], fdata['metadata']['grail_width'], 2 * fdata['metadata']['pocket_radius']],
        [tmp_tri_sha[0], tmp_tri_sha[1], tmp_tri_sha[2], tmp_tri_sha[3], tmp_tri_sha[4], tmp_tri_sha[5], tmp_tri_sha[6], tmp_tri_sha[7]],
        [-tmp_tri_sha[0], tmp_tri_sha[1], -tmp_tri_sha[2], tmp_tri_sha[3], -tmp_tri_sha[4], tmp_tri_sha[5], -tmp_tri_sha[6], tmp_tri_sha[7]],
        [-tmp_tri_sha[0], -tmp_tri_sha[1], -tmp_tri_sha[2], -tmp_tri_sha[3], -tmp_tri_sha[4], -tmp_tri_sha[5], -tmp_tri_sha[6], -tmp_tri_sha[7]],
        [tmp_tri_sha[0], -tmp_tri_sha[1], tmp_tri_sha[2], -tmp_tri_sha[3], tmp_tri_sha[4], -tmp_tri_sha[5], tmp_tri_sha[6], -tmp_tri_sha[7]],
    ];
    colorscheme = {
        'table_green_light': color(39, 144, 54),
        'table_green_dark': color(23, 104, 35),
        'table_wood': color(111, 16, 1),
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
    background('white');
    translate(cx, cy);

    // stopping the loop after receiving data and dont render anything till then
    if(pathdata.length > 0)
        noLoop();
    else
        return ;

    // drawing the table
    noStroke();
    // wood railing
    fill(colorscheme['table_wood']);
    srect(-(fdata['metadata']['table_width'] / 2) - fdata['metadata']['railing_width'], -(fdata['metadata']['table_height'] / 2) - fdata['metadata']['railing_width'], fdata['metadata']['table_width'] + 2 * fdata['metadata']['railing_width'], fdata['metadata']['table_height'] + 2 * fdata['metadata']['railing_width'], 15);
    // green railing
    fill(colorscheme['table_green_light']);
    srect(-(fdata['metadata']['table_width'] / 2) - fdata['metadata']['grail_width'], -(fdata['metadata']['table_height'] / 2) - fdata['metadata']['grail_width'], fdata['metadata']['table_width'] + 2 * fdata['metadata']['grail_width'], fdata['metadata']['table_height'] + 2 * fdata['metadata']['grail_width']);
    // green cloth
    fill(colorscheme['table_green_dark']);
    srect(-(fdata['metadata']['table_width'] / 2), -(fdata['metadata']['table_height'] / 2), fdata['metadata']['table_width'], fdata['metadata']['table_height']);
    // green shade points on cloth
    srect(fdata['shade_points'][0][0], -fdata['shade_points'][0][1], fdata['shade_points'][0][2], fdata['shade_points'][0][3]);
    srect(fdata['shade_points'][1][0], -fdata['shade_points'][1][1], fdata['shade_points'][1][2], fdata['shade_points'][1][3]);
    for(var i = 2;i <= 5;i ++)
        squad(fdata['shade_points'][i][0], -fdata['shade_points'][i][1], fdata['shade_points'][i][2], -fdata['shade_points'][i][3], fdata['shade_points'][i][4], -fdata['shade_points'][i][5], fdata['shade_points'][i][6], -fdata['shade_points'][i][7]);
    
    // drawing the pockets
    for(const [index, pocket] of fdata['pockets'].entries())
    {
        fill('white');
        sarc(pocket[0], -pocket[1], 2.4 * fdata['metadata']['pocket_radius'], 2.4 * fdata['metadata']['pocket_radius'], fdata['pockets_bound'][index][0], fdata['pockets_bound'][index][1], PIE);
        fill('black');
        scircle(pocket[0], -pocket[1], 2 * fdata['metadata']['pocket_radius']);
    }

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
                sarc(cbx, -cby, 2 * cbr, 2 * cbr, -(HALF_PI / 2), (HALF_PI / 2), CHORD);
                sarc(cbx, -cby, 2 * cbr, 2 * cbr, -(HALF_PI / 2) + PI, (HALF_PI / 2) + PI, CHORD);
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

function srect(x, y, wid, hei, cor=null)
{
    if(cor == null)
        rect(x * gscale, y * gscale, wid * gscale, hei * gscale);
    else
        rect(x * gscale, y * gscale, wid * gscale, hei * gscale, cor * gscale);
}

function scircle(x, y, dia)
{
    circle(x * gscale, y * gscale, dia * gscale);
}

function stext(strtext, x, y)
{
    text(strtext, x * gscale, y * gscale);
}

function sarc(x, y, w, h, start, stop, mode)
{
    arc(x * gscale, y * gscale, w * gscale, h * gscale, start, stop, mode);
}

function striangle(a, b, c, d, e, f)
{
    triangle(a * gscale, b * gscale, c * gscale, d * gscale, e * gscale, f * gscale);
}

function squad(x1, y1, x2, y2, x3, y3, x4, y4)
{
    quad(x1 * gscale, y1 * gscale, x2 * gscale, y2 * gscale, x3 * gscale, y3 * gscale, x4 * gscale, y4 * gscale);
}

