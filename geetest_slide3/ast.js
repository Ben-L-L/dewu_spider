const {parse} = require('@babel/parser');
const generator = require('@babel/generator').default;
const traverse = require('@babel/traverse').default;
const types = require('@babel/types'); //就是用来生成节点操作的
const fs = require('fs');


var jscode = fs.readFileSync('极验.js',{encoding:'utf-8'});
// console.log(jscode)
let AST_parse = parse(jscode);



let member_decode_js = '';
for (let i=0; i<=4; i++){
    member_decode_js+=generator(AST_parse.program.body[0].expression.callee.body.body[i],{compact:true}).code
    // delete AST_parse.program.body[i]


}

eval(member_decode_js);



const decrypt = {
    StringLiteral(path){
        // path.node.extra && delete path.node.extra
        path.node.extra && delete path.node.extra
    },
    CallExpression(path) {

        const node = path.node

        if (node.arguments.length !== 1 && !types.isNumericLiteral(node.arguments[0])) return

        const number = node.arguments[0].value
        if(typeof number !== "number") return;
        //# 修改函数名
        var value = AHkMb.DMF(number)
        console.log(types.valueToNode(value))
        // path.replaceWith(types.valueToNode(value))
    },
}

traverse(AST_parse, decrypt);

const js_code = generator(AST_parse,{compact:true}).code
// console.log(js_code)