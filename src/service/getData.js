import fetch from '../config/fetch'

/**
 * 主列表
 */

export const tableList = (index) => fetch('/tableList', {
    type: 'get',
    sort: index.sort,
    pageNumber: index.page.pageNumber,
    pageSize: index.page.pageSize,
    activeClass: String(index.activeClass),
    level: JSON.stringify(index.level),
    res_state: JSON.stringify(index.res_state),
    inputSearch: index.inputSearch,
    checkList:  JSON.stringify(index.checkList).replace(/\"/g,"'"),
});
/**
 * 详情列表
 */

export const operList = (index) => fetch('/operlist', {
    type: 'get',
    alert_id: index.id,
    idType: index.type,
    type_yj: index.type_yj,

    // activeClass: String(index.activeClass),
});
// 通报
export const parlist = (index) => fetch('/parlist', {
    type: 'get',
    alert_id: JSON.stringify(index.alert_id),
    // activeClass: String(index.activeClass),
});

// 标记
export const getMark = (id, val) => fetch('/mark', {
    type: 'get',
    id: id,
    val: val,
    // activeClass: String(index.activeClass),
});


// 提交通报
export const notification = (id) => fetch('/notification', {
    type: 'get',
    id: id,
    // activeClass: String(index.activeClass),
});


// 驗證
export const verification = (val) => fetch('/verification', {
    type: 'get',
    id: val.id,
    desc: val.desc,
    resource: val.resource,
    image: val.image,
    // activeClass: String(index.activeClass),
});

// 结束告警
export const endelarm = (id) => fetch('/endelarm', {
    type: 'get',
    id: JSON.stringify(id),
});




// 详情
export const getDetails = (lable, val, alert_id) => fetch('/details', {
    type: 'get',
    lable: lable,
    val: val,
    alert_id: alert_id,
    // activeClass: String(index.activeClass),
});


/**
 * 分类
 */

export const reasons = () => fetch('/reasons', {
    // type: 'hot'
});
