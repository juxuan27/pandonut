import feffery_antd_components as fac
from dash import html, dcc




def make_add_info_table() -> html.Div:

    return html.Div(
            children=[
                html.H1(id="add-info-title",children="信息添加"),
                html.P(id="add-info-explain",children='''
                        首先，我们对没能收集到您所在飞盘组织的信息表示诚挚歉意，同时也非常感谢您对我们的理解和支持！\n 请在下面的表格中填写相关信息，我们会以最快的速度将您的信息更新到地图上。❤️'''),
                html.P(id="add-info-explain-update",children=['''
                        如果您想查看更新记录，请点击''',
                        html.A(href="https://github.com/juxuan27/pandonut/blob/main/UPDATE.md",children="这里")]),
                html.Div(
                    className="add-info-form-container",
                    children=[
                        html.Div(id="show-info"),
                        html.Div(
                            className="add-info-form",
                            children=[
                                fac.AntdForm(
                                    [
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                id='form-usr-name',
                                            ),
                                            id='form-item-usr-name',
                                            label="您的称呼",
                                            required=True,
                                            tooltip="请输入您的昵称/姓名（如：“juju”）",
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                id='form-usr-contact',
                                            ),
                                            id='form-item-usr-contact',
                                            label="您的联系方式",
                                            required=True,
                                            tooltip="请输入您的联系方式（如：“wx：12345/tel：12345”）",
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                id='form-name',
                                            ),
                                            id='form-item-name',
                                            label="组织名称",
                                            required=True,
                                            tooltip="请输入您希望添加的组织名称（如：“TJUF——同济极限飞盘队”）",
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                id='form-type',
                                                placeholder='请选择组织类型',
                                                options=[
                                                    {'label': '学校队伍', 'value': '学校队伍'},
                                                    {'label': '女子队伍', 'value': '女子队伍'},
                                                    {'label': '混合/公开', 'value': '混合/公开'},
                                                    {'label': '青训队伍', 'value': '青训队伍'},
                                                    {'label': '其他', 'value': '其他'}
                                                ],
                                                style={
                                                    'width': '100%',
                                                    'text-align':'center',
                                                }
                                            ),
                                            id='form-item-type',
                                            label="组织类型",
                                            required=True,
                                            tooltip="请选择添加组织的组织类型（如：“学校队伍”）",
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                id='form-time',
                                            ),
                                            id='form-item-time',
                                            label="成立时间",
                                            tooltip="请输入该组织成立时间（如：“2015.6”）",
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                id='form-contact',
                                            ),
                                            id='form-item-contact',
                                            label="联系方式",
                                            required=True,
                                            tooltip="请输入该组织的联系方式（如：“wx：12345/tel：12345”）",
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                id='form-address',
                                            ),
                                            id='form-item-address',
                                            label="所在地址",
                                            required=True,
                                            tooltip="请输入该组织的常用地址（如：“中国上海市杨浦区四平路1239号同济大学”）",
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                id='form-compete',
                                                placeholder='请选择该组织是否为竞技性组织（是/否）',
                                                options=[
                                                    {'label': '是', 'value': '是'},
                                                    {'label': '否', 'value': '否'},
                                                ],
                                                style={
                                                    'width': '100%',
                                                    'text-align':'center',
                                                }
                                            ),
                                            id='form-item-compete',
                                            label="竞技组织",
                                            required=True,
                                            tooltip="请选择该组织是否为竞技性组织（是/否）",
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                id='form-coach',
                                            ),
                                            id='form-item-coach',
                                            label="组织教练",
                                            tooltip="请输入组织的组织者/教练，及其基本信息",
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                id='form-scale',
                                            ),
                                            id='form-item-scale',
                                            label="组织规模",
                                            tooltip="请输入组织的规模（如：“100-200人”）",
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                id='form-fee',
                                            ),
                                            id='form-item-fee',
                                            label="组织费用",
                                            tooltip="请输入参与该组织的费用（如：“30元/次”）",
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                id='form-other',
                                            ),
                                            id='form-item-other',
                                            label="其他信息",
                                            tooltip="请输入其他信息",
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdButton(
                                                '提交',
                                                type='primary',
                                                id='form-submit',
                                            ),
                                            wrapperCol={
                                                'offset': 12
                                            },
                                        )
                                        
                                    ],
                                    labelCol={
                                        'span': 5, 
                                    },
                                    wrapperCol={
                                        'span': 17, # 17/24
                                    },
                                )
                            ]

                        ),]
                    
                ),

            ],
            className="add-infor-container")
                            
