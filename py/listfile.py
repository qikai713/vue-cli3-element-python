# !/usr/bin/env python
# coding=utf-8

import json
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, g, request
from flask_cors import *
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.before_request
def before_request():
    print('连接到数据库...')
    g.conn = psycopg2.connect(host="10.255.81.44", port="5432", user="postgres", password="#$0okmNJI9~@$^hTC",
                              database="sa_data")
    g.cur = g.conn.cursor(cursor_factory=RealDictCursor)
    print('连接上了')


@app.teardown_request
def teardown_request(index):
    g.conn.commit()


@app.route('/tableList', methods=['GET'])
def get_data():
    try:

        search = request.args.get('search')
        sort = request.args.get('sort')
        inputSearch = request.args.get('inputSearch')
        pageSize = int(request.args.get('pageSize'))
        pageNumber = int(request.args.get('pageNumber'))
        dispose = request.args.get('dispose')
        activeClass_o = str(request.args.get('activeClass'))
        level = eval(request.args.get('level'))
        checkList = request.args.get('checkList')
        newLevel = 'and 1=1'
        newInputSearch = ''
        if activeClass_o == '全部':
            print '成功'
            activeClass = '1 = 1'
        else:
            print '失敗'
            activeClass = "alert_label like '%{0}%'".format(activeClass_o)

        if pageNumber != 1:
            pageNumber = pageNumber - 1
        else:
            pageNumber = 0
        if pageSize != 20:
            print pageSize
            pageSize = int(request.args.get('pageSize'))
        else:
            pageSize = 20
        if sort == 'descending':
            sort = 'order by new_time desc'
        elif sort == 'ascending':
            sort = 'order by new_time asc'
        else:
            sort = 'order by new_time desc'
        if level:
            level_string = ["or a.alert_level = '" + item + "'" for item in level]
            newLevel = 'and' + ' '.join(level_string)[2:]
        if inputSearch:
            newInputSearch = " and 1 = 1 and asset_name like '%{0}%' or domain like '%{1}%'".format(inputSearch,
                                                                                                    inputSearch)
        print ("""select a.alert_id,d2t(a.new_time) new_time,a.alert_label,a.alert_level,a.res_state,c.domain,c.asset_name,f.class_name,
            case when f.class_name = '硬件' then c.ip_addr when f.class_name = '服务' then c.website end as resource,
            case when a.res_state = '1' then '未处理' when res_state = '2' then '正在处理' when res_state = '3' then '已完成' end as res_state_pd,
            case when a.alert_level = '1' then '轻微' when a.alert_level = '2' then '低危' when a.alert_level = '3' then '中危' when a.alert_level = '4' then '高危' when a.alert_level = '5' then '严重'end as alert_level_pd
            from h_alert_info as a left join h_asset_alert as b on a.alert_id = b.alert_id left join h_asset_info as c on b.asset_id = c.asset_id
            left join k_asset_type as d on c.asset_type_id = d.asset_type_id left join k_asset_class as f on d.class_id = f.class_id where f.class_name in (select unnest(array{7})) and {4}  {5}{6} {0} limit {1} offset {2}*{3} """.format(
            sort, pageSize, pageNumber, pageSize, activeClass, newLevel, newInputSearch, checkList))

        g.cur.execute("""select distinct a.alert_id, h.fw_fz,h.fw_fm,z.yj_fz,z.yj_fm,d2t(a.new_time) new_time,a.alert_label,a.alert_level,a.res_state,c.domain,c.asset_name,f.class_name,
case when f.class_name = '硬件' then c.ip_addr when f.class_name = '服务' then c.website end as resource,
case when a.res_state = '1' then '未处理' when res_state = '2' then '正在处理' when res_state = '3' then '已完成' end as res_state_pd,
case when a.alert_level = '1' then '轻微' when a.alert_level = '2' then '低危' when a.alert_level = '3' then '中危' when a.alert_level = '4' then '高危' when a.alert_level = '5' then '严重'end as alert_level_pd
from h_alert_info as a left join h_asset_alert as b on a.alert_id = b.alert_id left join h_asset_info as c on b.asset_id = c.asset_id
left join k_asset_type as d on c.asset_type_id = d.asset_type_id
left join (select alert_id,sum(case when sign_result = '1' then 1  when sign_result = '' then 1 else 0 end)  as fw_fz,count(alert_id) as fw_fm from h_website_merge_info group by alert_id ) as h
on a.alert_id = h.alert_id
left join (select b.alert_id,a.id,sum(case when res_result = '误报' then 1  when res_result = '已处理' then 1 else 0 end)  as yj_fz,count(a.id) as yj_fm from h_response_cc_list as a left join h_alert_cc as b on b.id = a.id group by b.alert_id, a.id
) as z on a.alert_id = z.alert_id
left join k_asset_class as f on d.class_id = f.class_id left join h_website_merge_info as g on g.alert_id = a.alert_id  where f.class_name in (select unnest(array{7})) and {4}  {5}{6} {0} limit {1} offset {2}*{3} """.format(
            sort, pageSize, pageNumber, pageSize, activeClass, newLevel, newInputSearch, checkList))
        data_o = g.cur.fetchall()
        g.cur.execute("""select count(alert_id) from (select a.alert_id,d2t(a.new_time) new_time,a.alert_label,a.alert_level,a.res_state,c.asset_name,c.asset_level,c.uuid,c.domain ,c.in_charge ,c.asset_level ,f.class_name,
    case when f.class_name = '硬件' then c.ip_addr when f.class_name = '服务' then c.website end as resource,
    case when a.res_state = '1' then '未处理' when res_state = '2' then '正在处理' when res_state = '3' then '已完成' end as res_state_pd,
    case when a.alert_level = '1' then '轻微' when a.alert_level = '2' then '低危' when a.alert_level = '3' then '中危' when a.alert_level = '4' then '高危' when a.alert_level = '5' then '严重'end as alert_level_pd
    from h_alert_info as a left join h_asset_alert as b on a.alert_id = b.alert_id left join h_asset_info as c on b.asset_id = c.asset_id
    left join k_asset_type as d on c.asset_type_id = d.asset_type_id left join k_asset_class as f on d.class_id = f.class_id where {1} {0}) as fuucc""".format(
            sort, activeClass))
        data_t = g.cur.fetchone()['count']
        return json.dumps({'data': data_o, 'total': data_t, 'error': 'false'}, ensure_ascii=False)
    except Exception, e:
        return json.dumps({"error": "true", "msg": "查询失败", "warn": str(e)})



@app.route('/reasons', methods=['GET'])
def get_reasonsdata():
    try:
        g.cur.execute("""select
     sum(case when alert_label like '%终端发现恶意代码%' then 1 when alert_label like '%恶意代码网络传输%' then 1 else 0 end) as alert_label_a,
     sum(case when alert_label like '%C&C通讯%' then 1 else 0 end) as alert_label_b,
     sum(case when alert_label like '%网络入侵%' then 1 else 0 end) as alert_label_c,
     sum(case when alert_label like '%挂马%' then 1 else 0 end) as alert_label_d,
     sum(case when alert_label like '%钓鱼%' then 1 else 0 end) as alert_label_e,
     sum(case when alert_label like '%暗链%' then 1 else 0 end) as alert_label_f,
     sum(case when alert_label like '%WEB漏洞%' then 1 else 0 end) as alert_label_g,
     sum(case when alert_label like '%漏洞%' then 1 else 0 end) as alert_label_h,
     sum(case when alert_label like '%系统漏洞%' then 1 else 0 end) as alert_label_i,
     sum(case when alert_label like '%弱口令%' then 1 else 0 end) as alert_label_j,
     sum(case when alert_label like '%HTTP未响应%' then 1 else 0 end) as alert_label_k,
     sum(case when alert_label like '%DNS未响应%' then 1 else 0 end) as alert_label_l,
     sum(case when alert_label like '%PING未响应%' then 1 else 0 end) as alert_label_m,
     sum(case when alert_label like '%篡改%' then 1 else 0 end) as alert_label_n,
     sum(case when alert_label like '%敏感词%' then 1 else 0 end) as alert_label_o,
     sum(case when alert_label like '%违规接入%' then 1 else 0 end) as alert_label_p,
     sum(case when alert_label like '%违规外联%' then 1 else 0 end) as alert_label_q FROM h_alert_info""")
        data = g.cur.fetchall()
        return json.dumps({'data': data}, ensure_ascii=False)
    except Exception, e:
        return json.dumps({"error": "true", "msg": "查询失败", "warn": str(e)})


@app.route('/operlist', methods=['GET'])
def get_oper():
    try:
        alert_id = int(request.args.get('alert_id'))
        idType = int(request.args.get('idType'))
        type_yj = request.args.get('type_yj')
        if idType == 0:
            if type_yj == '恶意代码网络传输':
                print (
                    """select a.md5, a.virus_name, a.virus_family , a.is_notice_flag, b.deal_result, c.alert_label from h_alert_virus_hash as a left join h_response_md5_list as b on a.id = b.id left join h_alert_info as c on c.alert_id = a.alert_id where a.alert_id = '{0}'""".format(
                        alert_id))
                g.cur.execute(
                    """select a.md5, a.virus_name, a.virus_family , a.is_notice_flag, b.deal_result, c.alert_label from h_alert_virus_hash as a left join h_response_md5_list as b on a.id = b.id left join h_alert_info as c on c.alert_id = a.alert_id where a.alert_id = '{0}'""".format(
                        alert_id))
                data_z = g.cur.fetchall()
                return json.dumps(data_z, ensure_ascii=False)
            if type_yj == 'CC':
                print (
                    """select a.id,a.alert_id,a.cc_ip,a.connect_time,a.is_notice_flag, a.asset_ip,b.res_result, c.alert_label from h_alert_cc as a left join h_response_cc_list as b on a.id = b.id left join h_alert_info as c on c.alert_id = a.alert_id where a.alert_id = '{0}'""".format(
                        alert_id))
                g.cur.execute(
                    """select a.id,a.alert_id,a.cc_ip,a.connect_time,a.is_notice_flag, a.asset_ip,b.res_result,c.alert_label from h_alert_cc as a left join h_response_cc_list as b on a.id = b.id left join h_alert_info as c on c.alert_id = a.alert_id   where a.alert_id = '{0}'""".format(
                        alert_id))
                data_z = g.cur.fetchall()
                return json.dumps(data_z, ensure_ascii=False)
        if idType == 1:
            g.cur.execute(
                """select b.alert_reson, a.alert_id, d2t(b.new_time) as new_time,d2t(b.start_time) as start_time, b.website,a.res_state,
                case when b.is_notice_flag = false then '未通报' when b.is_notice_flag = true then '已通报' end as is_notice_flag_db,
                case when f.class_name = '硬件' then d.ip_addr when f.class_name = '服务' then d.website end as resource,
                b.is_notice_flag, b.sign_result, virus_url, b.loop_name, b.loop_level, b.loop_type,b.ip, b.sign_result, b.service, b.port,b.alert_merge_id,f.class_name  from h_alert_info as a left join h_website_merge_info as b on a.alert_id = b.alert_id left join
                  h_asset_alert as c on a.alert_id = c.alert_id left join h_asset_info as d on c.asset_id = d.asset_id
        left join k_asset_type as e on d.asset_type_id = e.asset_type_id left join k_asset_class as f on e.class_id = f.class_id
                  where a.alert_id = {0}""".format(
                    alert_id))
            data_z = g.cur.fetchall()
            return json.dumps(data_z, ensure_ascii=False)
    except Exception, e:
        return json.dumps({"error": "true", "msg": "查询失败", "warn": str(e)})

    else:
        g.cur.execute(
            """select b.alert_id,(b.new_time - b.start_time):: character varying(16) as duration ,b.connect_time,b.is_notice_flag,b.cc_dom from h_alert_info as a left join h_alert_cc as b on b.alert_id = a.alert_id
        where b.alert_id ={0}""".format(
                alert_id))
        data_z = g.cur.fetchall()
        return json.dumps(data_z, ensure_ascii=False)


@app.route('/parlist', methods=['GET'])
def get_par():
    try:
        alert_id = eval(request.args.get('alert_id'))
        print (
            """select b.alert_reson, a.alert_id, d2t(b.new_time) as new_time,d2t(b.start_time) as start_time, b.website,
            case when b.is_notice_flag = false then '未通报' when b.is_notice_flag = true then '已通报' end as is_notice_flag_db,
             case when i.class_name = '硬件' then d.ip_addr when i.class_name = '服务' then d.website end as resource,
            b.is_notice_flag, b.sign_result, virus_url, b.loop_name, b.loop_level, b.loop_type,b.ip, b.service, b.port,b.alert_merge_id, d.asset_name from    h_alert_info as a left join h_website_merge_info as b on a.alert_id = b.alert_id  left join h_asset_alert as c on c.alert_id = a.alert_id left join h_asset_info as d on c.asset_id = d.asset_id left join k_asset_type as g on d.asset_type_id = g.asset_type_id left join k_asset_class as i on g.class_id = i.class_id left join h_alert_cc as e on a.alert_id = e.alert_id left join h_alert_virus_hash as f on a.alert_id = e.alert_id where b.alert_id in (select unnest(array{0}))""".format(
                alert_id))
        g.cur.execute(
            """select b.alert_reson, a.alert_id, d2t(b.new_time) as new_time,d2t(b.start_time) as start_time, b.website,
            case when b.is_notice_flag = false then '未通报' when b.is_notice_flag = true then '已通报' end as is_notice_flag_db,
             case when i.class_name = '硬件' then d.ip_addr when i.class_name = '服务' then d.website end as resource,
            b.is_notice_flag, b.sign_result, virus_url, b.loop_name, b.loop_level, b.loop_type,b.ip, b.service, b.port,b.alert_merge_id, d.asset_name from    h_alert_info as a left join h_website_merge_info as b on a.alert_id = b.alert_id  left join h_asset_alert as c on c.alert_id = a.alert_id left join h_asset_info as d on c.asset_id = d.asset_id left join k_asset_type as g on d.asset_type_id = g.asset_type_id left join k_asset_class as i on g.class_id = i.class_id left join h_alert_cc as e on a.alert_id = e.alert_id left join h_alert_virus_hash as f on a.alert_id = e.alert_id where b.alert_id in (select unnest(array{0}))""".format(
                alert_id))
        data_z = g.cur.fetchall()
        return json.dumps(data_z, ensure_ascii=False)
    except Exception, e:
        return json.dumps({"error": "true", "msg": "查询失败", "warn": str(e)})
    g.commit.close()
    g.cur.close()
    g.conn.close()


@app.route('/addFlies', methods=['POST'])
def addfile():
    try:
        reqFile = request.files.get('file', None)
        print reqFile, '7777777'
        print os.path, '1111111111111'
        print os.path.join('..\..\..\image'), '55555555555555'

        if not reqFile:
            return json.dumps({"status": "fail", "msg": "未选择样本"})
        # reqFile.save(os.path.join('.\image'))
        return json.dumps({"error": "false", "data": "image"})
    except Exception, e:
        return json.dumps({"msg": "上传失败", "warn": str(e)})


# 标记
@app.route('/mark', methods=['GET'])
def get_mark():
    try:
        id = request.args.get('id')
        val = request.args.get('val')
        print id
        print val
        print (
            """UPDATE h_website_merge_info SET sign_result='{0}' WHERE alert_merge_id in (select unnest(array[{1}]))""".format(
                val, id))
        g.cur.execute(
            """UPDATE h_website_merge_info SET sign_result='{0}' WHERE alert_merge_id in (select unnest(array[{1}]))""".format(
                val, id))
        return json.dumps({"error": "false", "msg": "修改成功"})
    except Exception, e:
        return json.dumps({"error": "true", "msg": "查询失败", "warn": str(e)})
    g.commit.close()
    g.cur.close()
    g.conn.close()


# 提交通報
@app.route('/notification', methods=['GET'])
def get_notification():
    try:
        id = request.args.get('id')
        print id
        g.cur.execute(
            """UPDATE h_website_merge_info SET is_notice_flag='true' WHERE alert_merge_id in (select unnest(array[{0}]))""".format(
                id))
        return json.dumps({"error": "false", "msg": "提交成功"})
    except Exception, e:
        return json.dumps({"error": "true", "msg": "查询失败", "warn": str(e)})
    g.commit.close()
    g.conn.close()


# 结束告警
@app.route('/endelarm', methods=['GET'])
def get_endelarm():
    try:
        id = request.args.get('id')
        print id
        print (
            """UPDATE h_alert_info SET res_state='已完成' WHERE alert_merge_id in (select unnest(array{0}))""".format(id))
        return json.dumps({"error": "false", "msg": "提交成功"})
        g.cur.execute(
            """UPDATE h_alert_info SET res_state='已完成' WHERE alert_id in (select unnest(array{0}))""".format(id))
        return json.dumps({"error": "false", "msg": "提交成功"})
    except Exception, e:
        return json.dumps({"error": "true", "msg": "查询失败", "warn": str(e)})
    g.commit.close()
    g.cur.close()
    g.conn.close()


# 验证
@app.route('/verification', methods=['GET'])
def get_verification():
    try:
        id = request.args.get('id')
        desc = request.args.get('desc')
        resource = request.args.get('resource')
        image = request.args.get('image')
        print id
        print (
            """UPDATE h_website_merge_info SET address='{0}'', alert_validate_descr='{1}'', validate_state='{2}' WHERE alert_merge_id = '{3}'""".format(
                image, desc, resource, id))
        g.cur.execute(
            """UPDATE h_website_merge_info SET address='{0}', alert_validate_descr='{1}', validate_state='{2}' WHERE alert_merge_id = '{3}'""".format(
                image, desc, resource, id))
        return json.dumps({"error": "false", "msg": "提交成功"})
    except Exception, e:
        return json.dumps({"error": "true", "msg": "查询失败", "warn": str(e)})
    g.commit.close()
    g.cur.close()
    g.conn.close()


# 详情
@app.route('/details', methods=['GET'])
def get_details():
    try:
        lable = request.args.get('lable')
        alert_id = request.args.get('alert_id')
        val = request.args.get('val')
        if lable == 'false':
            newLable = "and is_notice_flag = '{0}'".format(lable)
        elif lable == 'true':
            newLable = "and is_notice_flag = '{0}'".format(lable)
        else:
            newLable = 'and 1=1'
        print alert_id
        print val
        print lable
        print """select b.alert_reson, a.alert_id, d2t(b.new_time) as new_time,d2t(b.start_time) as start_time, b.website,
                case when b.is_notice_flag = false then '未通报' when b.is_notice_flag = true then '已通报' end as is_notice_flag_db,
                b.is_notice_flag, b.sign_result, virus_url, b.loop_name, b.loop_level, b.loop_type,b.ip, b.sign_result, b.service, b.port,b.alert_merge_id,f.class_name  from h_alert_info as a left join h_website_merge_info as b on a.alert_id = b.alert_id left join
                  h_asset_alert as c on a.alert_id = c.alert_id left join h_asset_info as d on c.asset_id = d.asset_id
        left join k_asset_type as e on d.asset_type_id = e.asset_type_id left join k_asset_class as f on e.class_id = f.class_id
                  where a.alert_id = '{0}' and (alert_reson like '%{1}%' {2})""".format(alert_id, val, newLable)
        g.cur.execute(
            """select b.alert_reson, a.alert_id, d2t(b.new_time) as new_time,d2t(b.start_time) as start_time, b.website,
                case when b.is_notice_flag = false then '未通报' when b.is_notice_flag = true then '已通报' end as is_notice_flag_db,
                b.is_notice_flag, b.sign_result, virus_url, b.loop_name, b.loop_level, b.loop_type,b.ip, b.sign_result, b.service, b.port,b.alert_merge_id,f.class_name  from h_alert_info as a left join h_website_merge_info as b on a.alert_id = b.alert_id left join
                  h_asset_alert as c on a.alert_id = c.alert_id left join h_asset_info as d on c.asset_id = d.asset_id
        left join k_asset_type as e on d.asset_type_id = e.asset_type_id left join k_asset_class as f on e.class_id = f.class_id
                  where a.alert_id = '{0}' and (alert_reson like '%{1}%' {2})""".format(alert_id, val, newLable))
        data_d = g.cur.fetchall()
        return json.dumps(data_d, ensure_ascii=False)
    except Exception, e:
        return json.dumps({"error": "true", "msg": "查询失败", "warn": str(e)})



if __name__ == '__main__':
    app.run(port=5001, debug=True)
    # app.run(debug=True, threaded=True, port=5000, host="10.255.81.48")
