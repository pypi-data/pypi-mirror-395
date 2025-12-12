import ast
import copy

__all__ = [
    'AssignTransformer'

]


class AssignTransformer(ast.NodeTransformer):
    def generic_visit(self, node):
        ast.NodeTransformer.generic_visit(self, node)
        return node

    def gen_assign_checker_ast(self, node):
        if isinstance(node.targets[0], ast.Tuple):
            raise RuntimeError("unpacking during assignment is not supported")
        load_targets = []
        for target in node.targets:
            new_target = copy.deepcopy(target)
            new_target.ctx = ast.Load()
            load_targets.append(new_target)
        conditions = []
        for target in node.targets:
            load_target = copy.deepcopy(target)
            load_target.ctx = ast.Load()             
            if type(target) != ast.Attribute:
                conditions.append(ast.Call(func = ast.Name(id='hasattr', ctx=ast.Load()),
                                           args = [load_target, ast.Constant('_assign_')]))
            else:               
                conditions.append(ast.BoolOp(op = ast.And(),
                                             values = [ast.Call(func = ast.Name(id='hasattr', ctx=ast.Load()),
                                                                args = [load_target, ast.Constant('_assign_')]),
                                                       ast.BoolOp(op = ast.Or(),
                                                                  values = [ast.BoolOp(op = ast.And(),
                                                                                       values = [ast.Call(func = ast.Name(id='hasattr', ctx=ast.Load()),
                                                                                                          args = [load_target.value, ast.Constant('__dict__')]),
                                                                                                 ast.Compare(left = ast.Constant(load_target.attr),
                                                                                                             ops = [ast.In()],
                                                                                                             comparators = [ast.Attribute(value = load_target.value,
                                                                                                                                          attr = "__dict__",
                                                                                                                                          ctx = ast.Load())
                                                                                                                           ]
                                                                                                             )
                                                                                                ]
                                                                                       ),
                                                                            ast.Call(func = ast.Name(id = "hasattr", ctx = ast.Load()),
                                                                                     args = [ast.Attribute(value = ast.Call(func = ast.Name(id = "type", ctx = ast.Load()),
                                                                                                                            args = [load_target.value]),
                                                                                                           attr = load_target.attr,
                                                                                                           ctx = ast.Load()
                                                                                                           ),
                                                                                             ast.Constant("__get__")
                                                                                            ]
                                                                                    )
                                                                           ]
                                                                 )
                                                      ]
                                            )
                                 )
                
        new_node = ast.If(test = ast.Constant(True),
                          body = [ast.Try(body = [ast.Expr(load_target)],
                                          handlers = [ast.ExceptHandler(None,
                                                                        None,
                                                                        body = [ast.Assign(targets = [target],
                                                                                           value = node.value)
                                                                               ])
                                                     ],
                                          orelse = [ast.If(test = condition,
                                                           body = [ast.Assign(targets = [target],
                                                                              value = ast.Call(func = ast.Attribute(value = load_target,
                                                                                                                    attr = '_assign_',
                                                                                                                    ctx = ast.Load()),
                                                                                               args = [node.value],
                                                                                               keywords = [],
                                                                                               starargs = None,
                                                                                               kwargs = None)
                                                                              )
                                                                  ],
                                                           orelse = [ast.Assign(targets = [target],
                                                                                value = node.value)
                                                                    ])
                                                    ],
                                          finalbody = []) for target, load_target, condition in zip(node.targets, load_targets, conditions)
                                  ],
                          orelse = [])
        return new_node

    def gen_annassign_checker_ast(self, node):
        if node.value:
            target = node.target
            load_target = copy.deepcopy(node.target)
            load_target.ctx = ast.Load()
            if type(target) != ast.Attribute:
                condition = ast.Call(func = ast.Name(id='hasattr', ctx=ast.Load()),
                                     args = [load_target, ast.Constant('_assign_')])
            else:
                condition = ast.BoolOp(op = ast.And(),
                                       values = [ast.Call(func = ast.Name(id='hasattr', ctx=ast.Load()),
                                                          args = [load_target, ast.Constant('_assign_')]),
                                                 ast.BoolOp(op = ast.Or(),
                                                            values = [ast.BoolOp(op = ast.And(),
                                                                                 values = [ast.Call(func = ast.Name(id='hasattr', ctx=ast.Load()),
                                                                                                    args = [load_target.value, ast.Constant('__dict__')]),
                                                                                           ast.Compare(left = ast.Constant(load_target.attr),
                                                                                                       ops = [ast.In()],
                                                                                                       comparators = [ast.Attribute(value = load_target.value,
                                                                                                                                    attr = "__dict__",
                                                                                                                                    ctx = ast.Load())
                                                                                                                     ]
                                                                                                      )
                                                                                          ]
                                                                                ),
                                                                      ast.Call(func = ast.Name(id = "hasattr", ctx = ast.Load()),
                                                                               args = [ast.Attribute(value = ast.Call(func = ast.Name(id = "type", ctx = ast.Load()),
                                                                                                                      args = [load_target.value]),
                                                                                                     attr = load_target.attr,
                                                                                                     ctx = ast.Load()
                                                                                                    ),
                                                                                       ast.Constant("__get__")
                                                                                      ]
                                                                              )
                                                                     ]
                                                           )
                                                ]
                                      )
                                                             
            new_node = ast.If(test = ast.Constant(True),
                              body = [ast.Try(body = [ast.Expr(load_target)],
                                              handlers = [ast.ExceptHandler(None,
                                                                            None,
                                                                            body = [ast.AnnAssign(target = target,
                                                                                                  annotation = node.annotation,
                                                                                                  value = node.value,
                                                                                                  simple = node.simple)
                                                                                   ])
                                                         ],
                                              orelse = [ast.If(test = condition,
                                                               body = [ast.AnnAssign(target = target,
                                                                                     annotation = node.annotation,
                                                                                     value = ast.Call(func = ast.Attribute(value = load_target,
                                                                                                                           attr = '_assign_',
                                                                                                                           ctx = ast.Load()),
                                                                                                      args = [node.value, node.annotation],
                                                                                                      keywords = [],
                                                                                                      starargs = None,
                                                                                                      kwargs = None),
                                                                                     simple = node.simple
                                                                                     )
                                                                      ],
                                                               orelse = [ast.AnnAssign(target = target,
                                                                                       annotation = node.annotation,
                                                                                       value = node.value,
                                                                                       simple = node.simple)
                                                                        ])
                                                        ],
                                              finalbody = [])
                                      ],
                              orelse = [])
        else:
            new_node = node
        return new_node   

    def visit_Assign(self, node):       
        new_node = self.gen_assign_checker_ast(node)
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node

    def visit_AnnAssign(self, node):       
        new_node = self.gen_annassign_checker_ast(node)
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node

    def visit_NamedExpr(self, node):       
        raise RuntimeError("walrus operator is not supported")
    
