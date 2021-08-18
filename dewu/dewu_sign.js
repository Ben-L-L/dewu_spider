rpc.exports = {
    getnewsign: function (times, id,category,page,validate,chanllge) {
        //times: 系统当前时间戳
        //id: id号
        //category:类别 不同类别走不同方法
        //page : 页数 列表页和购买记录接口会用到
        //validate : 滑块验证会用到
        //chanllge： 滑块验证会用到
        var args_map = {};
        Java.perform(
            function () {
                if (category=='category') {
                    var obj = get_category(times, id)
                    args_map.sign = obj['sign']
                    args_map.times = obj['limet']

                }else if(category == 'list'){
                    var obj = get_list(times,id,page)
                    args_map.sign = obj['sign']
                    args_map.times = obj['limet']

                }else if(category == 'detial'){
                    var obj = get_detial(times,id)
                    args_map.sign = obj['sign']
                    args_map.times = obj['limet']
                }else if(category == 'history'){
                    var obj = get_history(times,id,page)
                    args_map.sign = obj['sign']
                    args_map.times = obj['limet']
                }else if(category == 'validate'){
                    var obj = get_validate(times,validate,chanllge)
                    args_map.sign = obj['sign']
                    args_map.times = obj['limet']
                }

            }
        )
        return args_map


    }
}



function get_category(times, id) {
    var DecodeUtils = Java.use('com.shizhuang.duapp.common.helper.net.DecodeUtils');
    var RequestUtils = Java.use('com.shizhuang.duapp.common.utils.RequestUtils');
    var InitService = Java.use('com.shizhuang.duapp.common.helper.InitService');
    var limet = times - InitService.i().g()
    // 定义一个HashMap类型
    var HashMap = Java.use('java.util.HashMap');
    //第一个参数 $new 实例化一个对象
    var hashmap_1 = HashMap.$new();
    if (id != undefined) {
        hashmap_1.put('catId', id + '')
    }
    var sign = RequestUtils.c(hashmap_1, limet)

    return {'sign':sign,'limet':limet}

}



function get_list(times, id,page) {
    var DecodeUtils = Java.use('com.shizhuang.duapp.common.helper.net.DecodeUtils');
    var RequestUtils = Java.use('com.shizhuang.duapp.common.utils.RequestUtils');
    var InitService = Java.use('com.shizhuang.duapp.common.helper.InitService');
    var limet = times - InitService.i().g()


    var AESEncrypt = Java.use('com.duapp.aesjni.AESEncrypt')

    var data = AESEncrypt.b('com.shizhuang.duapp.modules.app.DuApplication@188f615','aggregationfalsebrandId' + id + 'categoryIdscategoryLevel129debugAggtruefitIdslastId' + page +'limit20loginTokenplatformandroidpricepropertysortMode1sortType0timestamp' +limet + 'uuidd3912f6303c7eb8av4.60.1')

    var MD5Util = Java.use('com.shizhuang.duapp.framework.util.encrypt.MD5Util')
    var sign = MD5Util.a(data)
    return {'sign':sign,'limet':limet}


}



function get_detial(times,spuid){

    var DecodeUtils = Java.use('com.shizhuang.duapp.common.helper.net.DecodeUtils');
    var RequestUtils = Java.use('com.shizhuang.duapp.common.utils.RequestUtils');
    var InitService = Java.use('com.shizhuang.duapp.common.helper.InitService');
    var limet = times - InitService.i().g()

    var AESEncrypt = Java.use('com.duapp.aesjni.AESEncrypt')

    var data = AESEncrypt.b('com.shizhuang.duapp.modules.app.DuApplication@e4ba40c','arFileSwitchtruegroupFirstId' + spuid +'loginTokenplatformandroidproductSourceNamepropertyValueId0skuId0spuId' + spuid +'timestamp' + limet + 'uuidd3912f6303c7eb8av4.60.1')

    var MD5Util = Java.use('com.shizhuang.duapp.framework.util.encrypt.MD5Util')
    var sign = MD5Util.a(data)
    return {'sign':sign,'limet':limet}

}


function get_history(times, spuid,page) {
    var DecodeUtils = Java.use('com.shizhuang.duapp.common.helper.net.DecodeUtils');
    var RequestUtils = Java.use('com.shizhuang.duapp.common.utils.RequestUtils');
    var InitService = Java.use('com.shizhuang.duapp.common.helper.InitService');
    var limet = times - InitService.i().g()
    // 定义一个HashMap类型
    var HashMap = Java.use('java.util.HashMap');
    //第一个参数 $new 实例化一个对象
    var hashmap_1 = HashMap.$new();

    hashmap_1.put('lastId',page+'')
    hashmap_1.put('limit','100')
    hashmap_1.put('spuId',spuid+'')




    var sign = RequestUtils.c(hashmap_1, limet)

    return {'sign':sign,'limet':limet}

}


function get_validate(times, validate,chanllge) {
    var DecodeUtils = Java.use('com.shizhuang.duapp.common.helper.net.DecodeUtils');
    var RequestUtils = Java.use('com.shizhuang.duapp.common.utils.RequestUtils');
    var InitService = Java.use('com.shizhuang.duapp.common.helper.InitService');
    var limet = times - InitService.i().g()

    var AESEncrypt = Java.use('com.duapp.aesjni.AESEncrypt')

    var data = AESEncrypt.b('com.shizhuang.duapp.modules.app.DuApplication@e4ba40c','challenge' + chanllge +'loginTokenplatformandroidseccode' + validate + '|jordanserverStatus1timestamp' + limet + 'uuidd3912f6303c7eb8av4.60.1validate' + validate)

    var MD5Util = Java.use('com.shizhuang.duapp.framework.util.encrypt.MD5Util')
    var sign = MD5Util.a(data)

    return {'sign':sign,'limet':limet}
}

