from pooler.pooltable import PoolTable

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
    '2': [0, 50],
    },
}
tmp_bdist = fdata['metadata']['pocket_radius'] * (1 / 1.414)
fdata['pockets'] = [
    [-(fdata['metadata']['table_width'] / 2) - tmp_bdist,  (fdata['metadata']['table_height'] / 2) + tmp_bdist],
    [ (fdata['metadata']['table_width'] / 2) + tmp_bdist,  (fdata['metadata']['table_height'] / 2) + tmp_bdist],
    [ (fdata['metadata']['table_width'] / 2) + tmp_bdist, -(fdata['metadata']['table_height'] / 2) - tmp_bdist],
    [-(fdata['metadata']['table_width'] / 2) - tmp_bdist, -(fdata['metadata']['table_height'] / 2) - tmp_bdist],
    [0,  (fdata['metadata']['table_height'] / 2) + fdata['metadata']['pocket_radius']],
    [0, -(fdata['metadata']['table_height'] / 2) - fdata['metadata']['pocket_radius']],
    [ (fdata['metadata']['table_width'] / 2) + fdata['metadata']['pocket_radius'], 0],
    [-(fdata['metadata']['table_width'] / 2) - fdata['metadata']['pocket_radius'], 0],
]

pt = PoolTable(fdata)
pt.calculatePaths()
print(pt.getPaths())
