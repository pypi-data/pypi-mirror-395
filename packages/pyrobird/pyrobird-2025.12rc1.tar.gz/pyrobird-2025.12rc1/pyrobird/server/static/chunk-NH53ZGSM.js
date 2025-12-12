import{b as ze}from"./chunk-O3USTWPV.js";import{Aa as pt,Da as gt,Ga as Ct,Ha as Tt,R as _e,S as ht,V as Fe,fa as ut,ga as ft}from"./chunk-CYMI5ZNO.js";import{B as Q,D as Re,E as xt,J as B,Q as bt,R as Et,W as Dt,fa as wt,ha as oe,k as _t,ka as St,l as mt,n as b,o as G,oa as ae,p as re,pa as de,q as me,s as vt,x as yt,z as Ue}from"./chunk-7RYN5OS4.js";import{C as ke,Cc as lt,D as Ae,Eb as Be,Fb as m,G as N,Gb as z,Gc as Oe,Hb as at,Hc as ct,J as it,Jc as W,Kc as U,Nb as he,Ob as Le,Pb as ue,Sb as v,T as Ie,U as Z,Ub as M,V as k,Va as w,X as ee,Xb as dt,Yb as fe,Zb as ne,_a as ie,_b as se,bb as st,ca as nt,ea as c,eb as rt,ec as Pe,f as Y,g as D,gb as ce,h as Ze,hc as A,ic as pe,ja as P,jc as ge,ka as O,kb as H,l as f,mb as x,n as et,ob as F,pc as I,q as y,qb as ot,r as J,u as Ne,xa as te,y as tt,yb as j,za as le}from"./chunk-MIOPHATV.js";import{a as Ye,b as Je}from"./chunk-KYPE3LET.js";var Ke=class{dataNodes;expansionModel=new ze(!0);trackBy;getLevel;isExpandable;getChildren;toggle(n){this.expansionModel.toggle(this._trackByValue(n))}expand(n){this.expansionModel.select(this._trackByValue(n))}collapse(n){this.expansionModel.deselect(this._trackByValue(n))}isExpanded(n){return this.expansionModel.isSelected(this._trackByValue(n))}toggleDescendants(n){this.expansionModel.isSelected(this._trackByValue(n))?this.collapseDescendants(n):this.expandDescendants(n)}collapseAll(){this.expansionModel.clear()}expandDescendants(n){let e=[n];e.push(...this.getDescendants(n)),this.expansionModel.select(...e.map(i=>this._trackByValue(i)))}collapseDescendants(n){let e=[n];e.push(...this.getDescendants(n)),this.expansionModel.deselect(...e.map(i=>this._trackByValue(i)))}_trackByValue(n){return this.trackBy?this.trackBy(n):n}},ve=class extends Ke{getLevel;isExpandable;options;constructor(n,e,i){super(),this.getLevel=n,this.isExpandable=e,this.options=i,this.options&&(this.trackBy=this.options.trackBy)}getDescendants(n){let e=this.dataNodes.indexOf(n),i=[];for(let t=e+1;t<this.dataNodes.length&&this.getLevel(n)<this.getLevel(this.dataNodes[t]);t++)i.push(this.dataNodes[t]);return i}expandAll(){this.expansionModel.select(...this.dataNodes.map(n=>this._trackByValue(n)))}};var He=new nt("CDK_TREE_NODE_OUTLET_NODE"),ye=(()=>{class r{viewContainer=c(ce);_node=c(He,{optional:!0});constructor(){}static \u0275fac=function(i){return new(i||r)};static \u0275dir=x({type:r,selectors:[["","cdkTreeNodeOutlet",""]]})}return r})(),Ve=class{$implicit;level;index;count;constructor(n){this.$implicit=n}},xe=(()=>{class r{template=c(st);when;constructor(){}static \u0275fac=function(i){return new(i||r)};static \u0275dir=x({type:r,selectors:[["","cdkTreeNodeDef",""]],inputs:{when:[0,"cdkTreeNodeDefWhen","when"]}})}return r})();function Mt(){return Error("Could not find a tree control, levelAccessor, or childrenAccessor for the tree.")}var $=(()=>{class r{_differs=c(ct);_changeDetectorRef=c(Oe);_elementRef=c(le);_dir=c(Fe);_onDestroy=new Y;_dataDiffer;_defaultNodeDef;_dataSubscription;_levels=new Map;_parents=new Map;_ariaSets=new Map;get dataSource(){return this._dataSource}set dataSource(e){this._dataSource!==e&&this._switchDataSource(e)}_dataSource;treeControl;levelAccessor;childrenAccessor;trackBy;expansionKey;_nodeOutlet;_nodeDefs;viewChange=new D({start:0,end:Number.MAX_VALUE});_expansionModel;_flattenedNodes=new D([]);_nodeType=new D(null);_nodes=new D(new Map);_keyManagerNodes=new D([]);_keyManagerFactory=c(ht);_keyManager;_viewInit=!1;constructor(){}ngAfterContentInit(){this._initializeKeyManager()}ngAfterContentChecked(){this._updateDefaultNodeDefinition(),this._subscribeToDataChanges()}ngOnDestroy(){this._nodeOutlet.viewContainer.clear(),this._nodes.complete(),this._keyManagerNodes.complete(),this._nodeType.complete(),this._flattenedNodes.complete(),this.viewChange.complete(),this._onDestroy.next(),this._onDestroy.complete(),this._dataSource&&typeof this._dataSource.disconnect=="function"&&this.dataSource.disconnect(this),this._dataSubscription&&(this._dataSubscription.unsubscribe(),this._dataSubscription=null),this._keyManager?.destroy()}ngOnInit(){this._checkTreeControlUsage(),this._initializeDataDiffer()}ngAfterViewInit(){this._viewInit=!0}_updateDefaultNodeDefinition(){let e=this._nodeDefs.filter(i=>!i.when);e.length>1,this._defaultNodeDef=e[0]}_setNodeTypeIfUnset(e){this._nodeType.value===null&&this._nodeType.next(e)}_switchDataSource(e){this._dataSource&&typeof this._dataSource.disconnect=="function"&&this.dataSource.disconnect(this),this._dataSubscription&&(this._dataSubscription.unsubscribe(),this._dataSubscription=null),e||this._nodeOutlet.viewContainer.clear(),this._dataSource=e,this._nodeDefs&&this._subscribeToDataChanges()}_getExpansionModel(){return this.treeControl?this.treeControl.expansionModel:(this._expansionModel??=new ze(!0),this._expansionModel)}_subscribeToDataChanges(){if(this._dataSubscription)return;let e;ft(this._dataSource)?e=this._dataSource.connect(this):et(this._dataSource)?e=this._dataSource:Array.isArray(this._dataSource)&&(e=f(this._dataSource)),e&&(this._dataSubscription=this._getRenderData(e).pipe(k(this._onDestroy)).subscribe(i=>{this._renderDataChanges(i)}))}_getRenderData(e){let i=this._getExpansionModel();return J([e,this._nodeType,i.changed.pipe(Ie(null),ee(t=>{this._emitExpansionChanges(t)}))]).pipe(Z(([t,s])=>s===null?f({renderNodes:t,flattenedNodes:null,nodeType:s}):this._computeRenderingData(t,s).pipe(y(o=>Je(Ye({},o),{nodeType:s})))))}_renderDataChanges(e){if(e.nodeType===null){this.renderNodeChanges(e.renderNodes);return}this._updateCachedData(e.flattenedNodes),this.renderNodeChanges(e.renderNodes),this._updateKeyManagerItems(e.flattenedNodes)}_emitExpansionChanges(e){if(!e)return;let i=this._nodes.value;for(let t of e.added)i.get(t)?._emitExpansionState(!0);for(let t of e.removed)i.get(t)?._emitExpansionState(!1)}_initializeKeyManager(){let e=J([this._keyManagerNodes,this._nodes]).pipe(y(([t,s])=>t.reduce((o,a)=>{let d=s.get(this._getExpansionKey(a));return d&&o.push(d),o},[]))),i={trackBy:t=>this._getExpansionKey(t.data),skipPredicate:t=>!!t.isDisabled,typeAheadDebounceInterval:!0,horizontalOrientation:this._dir.value};this._keyManager=this._keyManagerFactory(e,i)}_initializeDataDiffer(){let e=this.trackBy??((i,t)=>this._getExpansionKey(t));this._dataDiffer=this._differs.find([]).create(e)}_checkTreeControlUsage(){}renderNodeChanges(e,i=this._dataDiffer,t=this._nodeOutlet.viewContainer,s){let o=i.diff(e);!o&&!this._viewInit||(o?.forEachOperation((a,d,l)=>{if(a.previousIndex==null)this.insertNode(e[l],l,t,s);else if(l==null)t.remove(d);else{let h=t.get(d);t.move(h,l)}}),o?.forEachIdentityChange(a=>{let d=a.item;if(a.currentIndex!=null){let l=t.get(a.currentIndex);l.context.$implicit=d}}),s?this._changeDetectorRef.markForCheck():this._changeDetectorRef.detectChanges())}_getNodeDef(e,i){if(this._nodeDefs.length===1)return this._nodeDefs.first;let t=this._nodeDefs.find(s=>s.when&&s.when(i,e))||this._defaultNodeDef;return t}insertNode(e,i,t,s){let o=this._getLevelAccessor(),a=this._getNodeDef(e,i),d=this._getExpansionKey(e),l=new Ve(e);l.index=i,s??=this._parents.get(d)??void 0,o?l.level=o(e):s!==void 0&&this._levels.has(this._getExpansionKey(s))?l.level=this._levels.get(this._getExpansionKey(s))+1:l.level=0,this._levels.set(d,l.level),(t||this._nodeOutlet.viewContainer).createEmbeddedView(a.template,l,i),R.mostRecentTreeNode&&(R.mostRecentTreeNode.data=e)}isExpanded(e){return!!(this.treeControl?.isExpanded(e)||this._expansionModel?.isSelected(this._getExpansionKey(e)))}toggle(e){this.treeControl?this.treeControl.toggle(e):this._expansionModel&&this._expansionModel.toggle(this._getExpansionKey(e))}expand(e){this.treeControl?this.treeControl.expand(e):this._expansionModel&&this._expansionModel.select(this._getExpansionKey(e))}collapse(e){this.treeControl?this.treeControl.collapse(e):this._expansionModel&&this._expansionModel.deselect(this._getExpansionKey(e))}toggleDescendants(e){this.treeControl?this.treeControl.toggleDescendants(e):this._expansionModel&&(this.isExpanded(e)?this.collapseDescendants(e):this.expandDescendants(e))}expandDescendants(e){if(this.treeControl)this.treeControl.expandDescendants(e);else if(this._expansionModel){let i=this._expansionModel;i.select(this._getExpansionKey(e)),this._getDescendants(e).pipe(N(1),k(this._onDestroy)).subscribe(t=>{i.select(...t.map(s=>this._getExpansionKey(s)))})}}collapseDescendants(e){if(this.treeControl)this.treeControl.collapseDescendants(e);else if(this._expansionModel){let i=this._expansionModel;i.deselect(this._getExpansionKey(e)),this._getDescendants(e).pipe(N(1),k(this._onDestroy)).subscribe(t=>{i.deselect(...t.map(s=>this._getExpansionKey(s)))})}}expandAll(){this.treeControl?this.treeControl.expandAll():this._expansionModel&&this._forEachExpansionKey(e=>this._expansionModel?.select(...e))}collapseAll(){this.treeControl?this.treeControl.collapseAll():this._expansionModel&&this._forEachExpansionKey(e=>this._expansionModel?.deselect(...e))}_getLevelAccessor(){return this.treeControl?.getLevel?.bind(this.treeControl)??this.levelAccessor}_getChildrenAccessor(){return this.treeControl?.getChildren?.bind(this.treeControl)??this.childrenAccessor}_getDirectChildren(e){let i=this._getLevelAccessor(),t=this._expansionModel??this.treeControl?.expansionModel;if(!t)return f([]);let s=this._getExpansionKey(e),o=t.changed.pipe(Z(d=>d.added.includes(s)?f(!0):d.removed.includes(s)?f(!1):Ze),Ie(this.isExpanded(e)));if(i)return J([o,this._flattenedNodes]).pipe(y(([d,l])=>d?this._findChildrenByLevel(i,l,e,1):[]));let a=this._getChildrenAccessor();if(a)return _e(a(e)??[]);throw Mt()}_findChildrenByLevel(e,i,t,s){let o=this._getExpansionKey(t),a=i.findIndex(u=>this._getExpansionKey(u)===o),d=e(t),l=d+s,h=[];for(let u=a+1;u<i.length;u++){let E=e(i[u]);if(E<=d)break;E<=l&&h.push(i[u])}return h}_registerNode(e){this._nodes.value.set(this._getExpansionKey(e.data),e),this._nodes.next(this._nodes.value)}_unregisterNode(e){this._nodes.value.delete(this._getExpansionKey(e.data)),this._nodes.next(this._nodes.value)}_getLevel(e){return this._levels.get(this._getExpansionKey(e))}_getSetSize(e){return this._getAriaSet(e).length}_getPositionInSet(e){let i=this._getAriaSet(e),t=this._getExpansionKey(e);return i.findIndex(s=>this._getExpansionKey(s)===t)+1}_getNodeParent(e){let i=this._parents.get(this._getExpansionKey(e.data));return i&&this._nodes.value.get(this._getExpansionKey(i))}_getNodeChildren(e){return this._getDirectChildren(e.data).pipe(y(i=>i.reduce((t,s)=>{let o=this._nodes.value.get(this._getExpansionKey(s));return o&&t.push(o),t},[])))}_sendKeydownToKeyManager(e){if(e.target===this._elementRef.nativeElement)this._keyManager.onKeydown(e);else{let i=this._nodes.getValue();for(let[,t]of i)if(e.target===t._elementRef.nativeElement){this._keyManager.onKeydown(e);break}}}_getDescendants(e){if(this.treeControl)return f(this.treeControl.getDescendants(e));if(this.levelAccessor){let i=this._findChildrenByLevel(this.levelAccessor,this._flattenedNodes.value,e,1/0);return f(i)}if(this.childrenAccessor)return this._getAllChildrenRecursively(e).pipe(ke((i,t)=>(i.push(...t),i),[]));throw Mt()}_getAllChildrenRecursively(e){return this.childrenAccessor?_e(this.childrenAccessor(e)).pipe(N(1),Z(i=>{for(let t of i)this._parents.set(this._getExpansionKey(t),e);return f(...i).pipe(Ae(t=>Ne(f([t]),this._getAllChildrenRecursively(t))))})):f([])}_getExpansionKey(e){return this.expansionKey?.(e)??e}_getAriaSet(e){let i=this._getExpansionKey(e),t=this._parents.get(i),s=t?this._getExpansionKey(t):null;return this._ariaSets.get(s)??[e]}_findParentForNode(e,i,t){if(!t.length)return null;let s=this._levels.get(this._getExpansionKey(e))??0;for(let o=i-1;o>=0;o--){let a=t[o];if((this._levels.get(this._getExpansionKey(a))??0)<s)return a}return null}_flattenNestedNodesWithExpansion(e,i=0){let t=this._getChildrenAccessor();return t?f(...e).pipe(Ae(s=>{let o=this._getExpansionKey(s);this._parents.has(o)||this._parents.set(o,null),this._levels.set(o,i);let a=_e(t(s));return Ne(f([s]),a.pipe(N(1),ee(d=>{this._ariaSets.set(o,[...d??[]]);for(let l of d??[]){let h=this._getExpansionKey(l);this._parents.set(h,s),this._levels.set(h,i+1)}}),Z(d=>d?this._flattenNestedNodesWithExpansion(d,i+1).pipe(y(l=>this.isExpanded(s)?l:[])):f([]))))}),ke((s,o)=>(s.push(...o),s),[])):f([...e])}_computeRenderingData(e,i){if(this.childrenAccessor&&i==="flat")return this._clearPreviousCache(),this._ariaSets.set(null,[...e]),this._flattenNestedNodesWithExpansion(e).pipe(y(t=>({renderNodes:t,flattenedNodes:t})));if(this.levelAccessor&&i==="nested"){let t=this.levelAccessor;return f(e.filter(s=>t(s)===0)).pipe(y(s=>({renderNodes:s,flattenedNodes:e})),ee(({flattenedNodes:s})=>{this._calculateParents(s)}))}else return i==="flat"?f({renderNodes:e,flattenedNodes:e}).pipe(ee(({flattenedNodes:t})=>{this._calculateParents(t)})):(this._clearPreviousCache(),this._ariaSets.set(null,[...e]),this._flattenNestedNodesWithExpansion(e).pipe(y(t=>({renderNodes:e,flattenedNodes:t}))))}_updateCachedData(e){this._flattenedNodes.next(e)}_updateKeyManagerItems(e){this._keyManagerNodes.next(e)}_calculateParents(e){let i=this._getLevelAccessor();if(i){this._clearPreviousCache();for(let t=0;t<e.length;t++){let s=e[t],o=this._getExpansionKey(s);this._levels.set(o,i(s));let a=this._findParentForNode(s,t,e);this._parents.set(o,a);let d=a?this._getExpansionKey(a):null,l=this._ariaSets.get(d)??[];l.splice(t,0,s),this._ariaSets.set(d,l)}}}_forEachExpansionKey(e){let i=[],t=[];this._nodes.value.forEach(s=>{i.push(this._getExpansionKey(s.data)),t.push(this._getDescendants(s.data))}),t.length>0?J(t).pipe(N(1),k(this._onDestroy)).subscribe(s=>{s.forEach(o=>o.forEach(a=>i.push(this._getExpansionKey(a)))),e(i)}):e(i)}_clearPreviousCache(){this._parents.clear(),this._levels.clear(),this._ariaSets.clear()}static \u0275fac=function(i){return new(i||r)};static \u0275cmp=H({type:r,selectors:[["cdk-tree"]],contentQueries:function(i,t,s){if(i&1&&dt(s,xe,5),i&2){let o;ne(o=se())&&(t._nodeDefs=o)}},viewQuery:function(i,t){if(i&1&&fe(ye,7),i&2){let s;ne(s=se())&&(t._nodeOutlet=s.first)}},hostAttrs:["role","tree",1,"cdk-tree"],hostBindings:function(i,t){i&1&&v("keydown",function(o){return t._sendKeydownToKeyManager(o)})},inputs:{dataSource:"dataSource",treeControl:"treeControl",levelAccessor:"levelAccessor",childrenAccessor:"childrenAccessor",trackBy:"trackBy",expansionKey:"expansionKey"},exportAs:["cdkTree"],decls:1,vars:0,consts:[["cdkTreeNodeOutlet",""]],template:function(i,t){i&1&&he(0,0)},dependencies:[ye],encapsulation:2})}return r})(),R=(()=>{class r{_elementRef=c(le);_tree=c($);_tabindex=-1;_type="flat";get role(){return"treeitem"}set role(e){}get isExpandable(){return this._isExpandable()}set isExpandable(e){this._inputIsExpandable=e,!(this.data&&!this._isExpandable||!this._inputIsExpandable)&&(this._inputIsExpanded?this.expand():this._inputIsExpanded===!1&&this.collapse())}get isExpanded(){return this._tree.isExpanded(this._data)}set isExpanded(e){this._inputIsExpanded=e,e?this.expand():this.collapse()}isDisabled;typeaheadLabel;getLabel(){return this.typeaheadLabel||this._elementRef.nativeElement.textContent?.trim()||""}activation=new ie;expandedChange=new ie;static mostRecentTreeNode=null;_destroyed=new Y;_dataChanges=new Y;_inputIsExpandable=!1;_inputIsExpanded=void 0;_shouldFocus=!0;_parentNodeAriaLevel;get data(){return this._data}set data(e){e!==this._data&&(this._data=e,this._dataChanges.next())}_data;get isLeafNode(){return this._tree.treeControl?.isExpandable!==void 0&&!this._tree.treeControl.isExpandable(this._data)?!0:this._tree.treeControl?.isExpandable===void 0&&this._tree.treeControl?.getDescendants(this._data).length===0}get level(){return this._tree._getLevel(this._data)??this._parentNodeAriaLevel}_isExpandable(){return this._tree.treeControl?!this.isLeafNode:this._inputIsExpandable}_getAriaExpanded(){return this._isExpandable()?String(this.isExpanded):null}_getSetSize(){return this._tree._getSetSize(this._data)}_getPositionInSet(){return this._tree._getPositionInSet(this._data)}_changeDetectorRef=c(Oe);constructor(){r.mostRecentTreeNode=this}ngOnInit(){this._parentNodeAriaLevel=Gt(this._elementRef.nativeElement),this._tree._getExpansionModel().changed.pipe(y(()=>this.isExpanded),it(),k(this._destroyed)).pipe(k(this._destroyed)).subscribe(()=>this._changeDetectorRef.markForCheck()),this._tree._setNodeTypeIfUnset(this._type),this._tree._registerNode(this)}ngOnDestroy(){r.mostRecentTreeNode===this&&(r.mostRecentTreeNode=null),this._dataChanges.complete(),this._destroyed.next(),this._destroyed.complete()}getParent(){return this._tree._getNodeParent(this)??null}getChildren(){return this._tree._getNodeChildren(this)}focus(){this._tabindex=0,this._shouldFocus&&this._elementRef.nativeElement.focus(),this._changeDetectorRef.markForCheck()}unfocus(){this._tabindex=-1,this._changeDetectorRef.markForCheck()}activate(){this.isDisabled||this.activation.next(this._data)}collapse(){this.isExpandable&&this._tree.collapse(this._data)}expand(){this.isExpandable&&this._tree.expand(this._data)}makeFocusable(){this._tabindex=0,this._changeDetectorRef.markForCheck()}_focusItem(){this.isDisabled||this._tree._keyManager.focusItem(this)}_setActiveItem(){this.isDisabled||(this._shouldFocus=!1,this._tree._keyManager.focusItem(this),this._shouldFocus=!0)}_emitExpansionState(e){this.expandedChange.emit(e)}static \u0275fac=function(i){return new(i||r)};static \u0275dir=x({type:r,selectors:[["cdk-tree-node"]],hostAttrs:["role","treeitem",1,"cdk-tree-node"],hostVars:5,hostBindings:function(i,t){i&1&&v("click",function(){return t._setActiveItem()})("focus",function(){return t._focusItem()}),i&2&&(ue("tabIndex",t._tabindex),j("aria-expanded",t._getAriaExpanded())("aria-level",t.level+1)("aria-posinset",t._getPositionInSet())("aria-setsize",t._getSetSize()))},inputs:{role:"role",isExpandable:[2,"isExpandable","isExpandable",W],isExpanded:"isExpanded",isDisabled:[2,"isDisabled","isDisabled",W],typeaheadLabel:[0,"cdkTreeNodeTypeaheadLabel","typeaheadLabel"]},outputs:{activation:"activation",expandedChange:"expandedChange"},exportAs:["cdkTreeNode"]})}return r})();function Gt(r){let n=r.parentElement;for(;n&&!Qt(n);)n=n.parentElement;return n?n.classList.contains("cdk-nested-tree-node")?U(n.getAttribute("aria-level")):0:-1}function Qt(r){let n=r.classList;return!!(n?.contains("cdk-nested-tree-node")||n?.contains("cdk-tree"))}var $t=/([A-Za-z%]+)$/,je=(()=>{class r{_treeNode=c(R);_tree=c($);_element=c(le);_dir=c(Fe,{optional:!0});_currentPadding;_destroyed=new Y;indentUnits="px";get level(){return this._level}set level(e){this._setLevelInput(e)}_level;get indent(){return this._indent}set indent(e){this._setIndentInput(e)}_indent=40;constructor(){this._setPadding(),this._dir?.change.pipe(k(this._destroyed)).subscribe(()=>this._setPadding(!0)),this._treeNode._dataChanges.subscribe(()=>this._setPadding())}ngOnDestroy(){this._destroyed.next(),this._destroyed.complete()}_paddingIndent(){let e=(this._treeNode.data&&this._tree._getLevel(this._treeNode.data))??null,i=this._level==null?e:this._level;return typeof i=="number"?`${i*this._indent}${this.indentUnits}`:null}_setPadding(e=!1){let i=this._paddingIndent();if(i!==this._currentPadding||e){let t=this._element.nativeElement,s=this._dir&&this._dir.value==="rtl"?"paddingRight":"paddingLeft",o=s==="paddingLeft"?"paddingRight":"paddingLeft";t.style[s]=i||"",t.style[o]="",this._currentPadding=i}}_setLevelInput(e){this._level=isNaN(e)?null:e,this._setPadding()}_setIndentInput(e){let i=e,t="px";if(typeof e=="string"){let s=e.split($t);i=s[0],t=s[1]||t}this.indentUnits=t,this._indent=U(i),this._setPadding()}static \u0275fac=function(i){return new(i||r)};static \u0275dir=x({type:r,selectors:[["","cdkTreeNodePadding",""]],inputs:{level:[2,"cdkTreeNodePadding","level",U],indent:[0,"cdkTreeNodePaddingIndent","indent"]}})}return r})(),We=(()=>{class r{_tree=c($);_treeNode=c(R);recursive=!1;constructor(){}_toggle(){this.recursive?this._tree.toggleDescendants(this._treeNode.data):this._tree.toggle(this._treeNode.data),this._tree._keyManager.focusItem(this._treeNode)}static \u0275fac=function(i){return new(i||r)};static \u0275dir=x({type:r,selectors:[["","cdkTreeNodeToggle",""]],hostAttrs:["tabindex","-1"],hostBindings:function(i,t){i&1&&v("click",function(o){return t._toggle(),o.stopPropagation()})("keydown.Enter",function(o){return t._toggle(),o.preventDefault()})("keydown.Space",function(o){return t._toggle(),o.preventDefault()})},inputs:{recursive:[2,"cdkTreeNodeToggleRecursive","recursive",W]}})}return r})();function qt(r){return!!r._isNoopTreeKeyManager}var At=(()=>{class r extends R{get tabIndexInputBinding(){return this._tabIndexInputBinding}set tabIndexInputBinding(e){this._tabIndexInputBinding=e}_tabIndexInputBinding;defaultTabIndex=0;_getTabindexAttribute(){return qt(this._tree._keyManager)?this.tabIndexInputBinding:this._tabindex}get disabled(){return this.isDisabled}set disabled(e){this.isDisabled=e}constructor(){super();let e=c(new lt("tabindex"),{optional:!0});this.tabIndexInputBinding=Number(e)||this.defaultTabIndex}ngOnInit(){super.ngOnInit()}ngOnDestroy(){super.ngOnDestroy()}static \u0275fac=function(i){return new(i||r)};static \u0275dir=x({type:r,selectors:[["mat-tree-node"]],hostAttrs:[1,"mat-tree-node"],hostVars:5,hostBindings:function(i,t){i&1&&v("click",function(){return t._focusItem()}),i&2&&(ue("tabIndex",t._getTabindexAttribute()),j("aria-expanded",t._getAriaExpanded())("aria-level",t.level+1)("aria-posinset",t._getPositionInSet())("aria-setsize",t._getSetSize()))},inputs:{tabIndexInputBinding:[2,"tabIndex","tabIndexInputBinding",e=>e==null?0:U(e)],disabled:[2,"disabled","disabled",W]},outputs:{activation:"activation",expandedChange:"expandedChange"},exportAs:["matTreeNode"],features:[I([{provide:R,useExisting:r}]),F]})}return r})(),It=(()=>{class r extends xe{data;static \u0275fac=(()=>{let e;return function(t){return(e||(e=te(r)))(t||r)}})();static \u0275dir=x({type:r,selectors:[["","matTreeNodeDef",""]],inputs:{when:[0,"matTreeNodeDefWhen","when"],data:[0,"matTreeNode","data"]},features:[I([{provide:xe,useExisting:r}]),F]})}return r})();var Bt=(()=>{class r extends je{get level(){return this._level}set level(e){this._setLevelInput(e)}get indent(){return this._indent}set indent(e){this._setIndentInput(e)}static \u0275fac=(()=>{let e;return function(t){return(e||(e=te(r)))(t||r)}})();static \u0275dir=x({type:r,selectors:[["","matTreeNodePadding",""]],inputs:{level:[2,"matTreeNodePadding","level",U],indent:[0,"matTreeNodePaddingIndent","indent"]},features:[I([{provide:je,useExisting:r}]),F]})}return r})(),kt=(()=>{class r{viewContainer=c(ce);_node=c(He,{optional:!0});static \u0275fac=function(i){return new(i||r)};static \u0275dir=x({type:r,selectors:[["","matTreeNodeOutlet",""]],features:[I([{provide:ye,useExisting:r}])]})}return r})(),Lt=(()=>{class r extends ${_nodeOutlet=void 0;static \u0275fac=(()=>{let e;return function(t){return(e||(e=te(r)))(t||r)}})();static \u0275cmp=H({type:r,selectors:[["mat-tree"]],viewQuery:function(i,t){if(i&1&&fe(kt,7),i&2){let s;ne(s=se())&&(t._nodeOutlet=s.first)}},hostAttrs:[1,"mat-tree"],exportAs:["matTree"],features:[I([{provide:$,useExisting:r}]),F],decls:1,vars:0,consts:[["matTreeNodeOutlet",""]],template:function(i,t){i&1&&he(0,0)},dependencies:[kt],styles:[`.mat-tree{display:block;background-color:var(--mat-tree-container-background-color, var(--mat-sys-surface))}.mat-tree-node,.mat-nested-tree-node{color:var(--mat-tree-node-text-color, var(--mat-sys-on-surface));font-family:var(--mat-tree-node-text-font, var(--mat-sys-body-large-font));font-size:var(--mat-tree-node-text-size, var(--mat-sys-body-large-size));font-weight:var(--mat-tree-node-text-weight, var(--mat-sys-body-large-weight))}.mat-tree-node{display:flex;align-items:center;flex:1;word-wrap:break-word;min-height:var(--mat-tree-node-min-height, 48px)}.mat-nested-tree-node{border-bottom-width:0}
`],encapsulation:2})}return r})(),Pt=(()=>{class r extends We{static \u0275fac=(()=>{let e;return function(t){return(e||(e=te(r)))(t||r)}})();static \u0275dir=x({type:r,selectors:[["","matTreeNodeToggle",""]],inputs:{recursive:[0,"matTreeNodeToggleRecursive","recursive"]},features:[I([{provide:We,useExisting:r}]),F]})}return r})();var be=class{transformFunction;getLevel;isExpandable;getChildren;constructor(n,e,i,t){this.transformFunction=n,this.getLevel=e,this.isExpandable=i,this.getChildren=t}_flattenNode(n,e,i,t){let s=this.transformFunction(n,e);if(i.push(s),this.isExpandable(s)){let o=this.getChildren(n);o&&(Array.isArray(o)?this._flattenChildren(o,e,i,t):o.pipe(N(1)).subscribe(a=>{this._flattenChildren(a,e,i,t)}))}return i}_flattenChildren(n,e,i,t){n.forEach((s,o)=>{let a=t.slice();a.push(o!=n.length-1),this._flattenNode(s,e+1,i,a)})}flattenNodes(n){let e=[];return n.forEach(i=>this._flattenNode(i,0,e,[])),e}expandFlattenedNodes(n,e){let i=[],t=[];return t[0]=!0,n.forEach(s=>{let o=!0;for(let a=0;a<=this.getLevel(s);a++)o=o&&t[a];o&&i.push(s),this.isExpandable(s)&&(t[this.getLevel(s)+1]=e.isExpanded(s))}),i}},Ee=class extends ut{_treeControl;_treeFlattener;_flattenedData=new D([]);_expandedData=new D([]);get data(){return this._data.value}set data(n){this._data.next(n),this._flattenedData.next(this._treeFlattener.flattenNodes(this.data)),this._treeControl.dataNodes=this._flattenedData.value}_data=new D([]);constructor(n,e,i){super(),this._treeControl=n,this._treeFlattener=e,i&&(this.data=i)}connect(n){return tt(n.viewChange,this._treeControl.expansionModel.changed,this._flattenedData).pipe(y(()=>(this._expandedData.next(this._treeFlattener.expandFlattenedNodes(this._flattenedData.value,this._treeControl)),this._expandedData.value)))}disconnect(){}};var Ot=new re,De=new b,q=class extends wt{constructor(){super(),this.isLineSegmentsGeometry=!0,this.type="LineSegmentsGeometry";let n=[-1,2,0,1,2,0,-1,1,0,1,1,0,-1,0,0,1,0,0,-1,-1,0,1,-1,0],e=[-1,2,1,2,-1,1,1,1,-1,-1,1,-1,-1,-2,1,-2],i=[0,2,1,2,3,1,2,4,3,4,5,3,4,6,5,6,7,5];this.setIndex(i),this.setAttribute("position",new Ue(n,3)),this.setAttribute("uv",new Ue(e,2))}applyMatrix4(n){let e=this.attributes.instanceStart,i=this.attributes.instanceEnd;return e!==void 0&&(e.applyMatrix4(n),i.applyMatrix4(n),e.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}setPositions(n){let e;n instanceof Float32Array?e=n:Array.isArray(n)&&(e=new Float32Array(n));let i=new oe(e,6,1);return this.setAttribute("instanceStart",new B(i,3,0)),this.setAttribute("instanceEnd",new B(i,3,3)),this.instanceCount=this.attributes.instanceStart.count,this.computeBoundingBox(),this.computeBoundingSphere(),this}setColors(n){let e;n instanceof Float32Array?e=n:Array.isArray(n)&&(e=new Float32Array(n));let i=new oe(e,6,1);return this.setAttribute("instanceColorStart",new B(i,3,0)),this.setAttribute("instanceColorEnd",new B(i,3,3)),this}fromWireframeGeometry(n){return this.setPositions(n.attributes.position.array),this}fromEdgesGeometry(n){return this.setPositions(n.attributes.position.array),this}fromMesh(n){return this.fromWireframeGeometry(new Dt(n.geometry)),this}fromLineSegments(n){let e=n.geometry;return this.setPositions(e.attributes.position.array),this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new re);let n=this.attributes.instanceStart,e=this.attributes.instanceEnd;n!==void 0&&e!==void 0&&(this.boundingBox.setFromBufferAttribute(n),Ot.setFromBufferAttribute(e),this.boundingBox.union(Ot))}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new me),this.boundingBox===null&&this.computeBoundingBox();let n=this.attributes.instanceStart,e=this.attributes.instanceEnd;if(n!==void 0&&e!==void 0){let i=this.boundingSphere.center;this.boundingBox.getCenter(i);let t=0;for(let s=0,o=n.count;s<o;s++)De.fromBufferAttribute(n,s),t=Math.max(t,i.distanceToSquared(De)),De.fromBufferAttribute(e,s),t=Math.max(t,i.distanceToSquared(De));this.boundingSphere.radius=Math.sqrt(t),isNaN(this.boundingSphere.radius)&&console.error("THREE.LineSegmentsGeometry.computeBoundingSphere(): Computed radius is NaN. The instanced position data is likely to have NaN values.",this)}}toJSON(){}};ae.line={worldUnits:{value:1},linewidth:{value:1},resolution:{value:new mt(1,1)},dashOffset:{value:0},dashScale:{value:1},dashSize:{value:1},gapSize:{value:1}};de.line={uniforms:Re.merge([ae.common,ae.fog,ae.line]),vertexShader:`
		#include <common>
		#include <color_pars_vertex>
		#include <fog_pars_vertex>
		#include <logdepthbuf_pars_vertex>
		#include <clipping_planes_pars_vertex>

		uniform float linewidth;
		uniform vec2 resolution;

		attribute vec3 instanceStart;
		attribute vec3 instanceEnd;

		attribute vec3 instanceColorStart;
		attribute vec3 instanceColorEnd;

		#ifdef WORLD_UNITS

			varying vec4 worldPos;
			varying vec3 worldStart;
			varying vec3 worldEnd;

			#ifdef USE_DASH

				varying vec2 vUv;

			#endif

		#else

			varying vec2 vUv;

		#endif

		#ifdef USE_DASH

			uniform float dashScale;
			attribute float instanceDistanceStart;
			attribute float instanceDistanceEnd;
			varying float vLineDistance;

		#endif

		void trimSegment( const in vec4 start, inout vec4 end ) {

			// trim end segment so it terminates between the camera plane and the near plane

			// conservative estimate of the near plane
			float a = projectionMatrix[ 2 ][ 2 ]; // 3nd entry in 3th column
			float b = projectionMatrix[ 3 ][ 2 ]; // 3nd entry in 4th column
			float nearEstimate = - 0.5 * b / a;

			float alpha = ( nearEstimate - start.z ) / ( end.z - start.z );

			end.xyz = mix( start.xyz, end.xyz, alpha );

		}

		void main() {

			#ifdef USE_COLOR

				vColor.xyz = ( position.y < 0.5 ) ? instanceColorStart : instanceColorEnd;

			#endif

			#ifdef USE_DASH

				vLineDistance = ( position.y < 0.5 ) ? dashScale * instanceDistanceStart : dashScale * instanceDistanceEnd;
				vUv = uv;

			#endif

			float aspect = resolution.x / resolution.y;

			// camera space
			vec4 start = modelViewMatrix * vec4( instanceStart, 1.0 );
			vec4 end = modelViewMatrix * vec4( instanceEnd, 1.0 );

			#ifdef WORLD_UNITS

				worldStart = start.xyz;
				worldEnd = end.xyz;

			#else

				vUv = uv;

			#endif

			// special case for perspective projection, and segments that terminate either in, or behind, the camera plane
			// clearly the gpu firmware has a way of addressing this issue when projecting into ndc space
			// but we need to perform ndc-space calculations in the shader, so we must address this issue directly
			// perhaps there is a more elegant solution -- WestLangley

			bool perspective = ( projectionMatrix[ 2 ][ 3 ] == - 1.0 ); // 4th entry in the 3rd column

			if ( perspective ) {

				if ( start.z < 0.0 && end.z >= 0.0 ) {

					trimSegment( start, end );

				} else if ( end.z < 0.0 && start.z >= 0.0 ) {

					trimSegment( end, start );

				}

			}

			// clip space
			vec4 clipStart = projectionMatrix * start;
			vec4 clipEnd = projectionMatrix * end;

			// ndc space
			vec3 ndcStart = clipStart.xyz / clipStart.w;
			vec3 ndcEnd = clipEnd.xyz / clipEnd.w;

			// direction
			vec2 dir = ndcEnd.xy - ndcStart.xy;

			// account for clip-space aspect ratio
			dir.x *= aspect;
			dir = normalize( dir );

			#ifdef WORLD_UNITS

				vec3 worldDir = normalize( end.xyz - start.xyz );
				vec3 tmpFwd = normalize( mix( start.xyz, end.xyz, 0.5 ) );
				vec3 worldUp = normalize( cross( worldDir, tmpFwd ) );
				vec3 worldFwd = cross( worldDir, worldUp );
				worldPos = position.y < 0.5 ? start: end;

				// height offset
				float hw = linewidth * 0.5;
				worldPos.xyz += position.x < 0.0 ? hw * worldUp : - hw * worldUp;

				// don't extend the line if we're rendering dashes because we
				// won't be rendering the endcaps
				#ifndef USE_DASH

					// cap extension
					worldPos.xyz += position.y < 0.5 ? - hw * worldDir : hw * worldDir;

					// add width to the box
					worldPos.xyz += worldFwd * hw;

					// endcaps
					if ( position.y > 1.0 || position.y < 0.0 ) {

						worldPos.xyz -= worldFwd * 2.0 * hw;

					}

				#endif

				// project the worldpos
				vec4 clip = projectionMatrix * worldPos;

				// shift the depth of the projected points so the line
				// segments overlap neatly
				vec3 clipPose = ( position.y < 0.5 ) ? ndcStart : ndcEnd;
				clip.z = clipPose.z * clip.w;

			#else

				vec2 offset = vec2( dir.y, - dir.x );
				// undo aspect ratio adjustment
				dir.x /= aspect;
				offset.x /= aspect;

				// sign flip
				if ( position.x < 0.0 ) offset *= - 1.0;

				// endcaps
				if ( position.y < 0.0 ) {

					offset += - dir;

				} else if ( position.y > 1.0 ) {

					offset += dir;

				}

				// adjust for linewidth
				offset *= linewidth;

				// adjust for clip-space to screen-space conversion // maybe resolution should be based on viewport ...
				offset /= resolution.y;

				// select end
				vec4 clip = ( position.y < 0.5 ) ? clipStart : clipEnd;

				// back to clip space
				offset *= clip.w;

				clip.xy += offset;

			#endif

			gl_Position = clip;

			vec4 mvPosition = ( position.y < 0.5 ) ? start : end; // this is an approximation

			#include <logdepthbuf_vertex>
			#include <clipping_planes_vertex>
			#include <fog_vertex>

		}
		`,fragmentShader:`
		uniform vec3 diffuse;
		uniform float opacity;
		uniform float linewidth;

		#ifdef USE_DASH

			uniform float dashOffset;
			uniform float dashSize;
			uniform float gapSize;

		#endif

		varying float vLineDistance;

		#ifdef WORLD_UNITS

			varying vec4 worldPos;
			varying vec3 worldStart;
			varying vec3 worldEnd;

			#ifdef USE_DASH

				varying vec2 vUv;

			#endif

		#else

			varying vec2 vUv;

		#endif

		#include <common>
		#include <color_pars_fragment>
		#include <fog_pars_fragment>
		#include <logdepthbuf_pars_fragment>
		#include <clipping_planes_pars_fragment>

		vec2 closestLineToLine(vec3 p1, vec3 p2, vec3 p3, vec3 p4) {

			float mua;
			float mub;

			vec3 p13 = p1 - p3;
			vec3 p43 = p4 - p3;

			vec3 p21 = p2 - p1;

			float d1343 = dot( p13, p43 );
			float d4321 = dot( p43, p21 );
			float d1321 = dot( p13, p21 );
			float d4343 = dot( p43, p43 );
			float d2121 = dot( p21, p21 );

			float denom = d2121 * d4343 - d4321 * d4321;

			float numer = d1343 * d4321 - d1321 * d4343;

			mua = numer / denom;
			mua = clamp( mua, 0.0, 1.0 );
			mub = ( d1343 + d4321 * ( mua ) ) / d4343;
			mub = clamp( mub, 0.0, 1.0 );

			return vec2( mua, mub );

		}

		void main() {

			float alpha = opacity;
			vec4 diffuseColor = vec4( diffuse, alpha );

			#include <clipping_planes_fragment>

			#ifdef USE_DASH

				if ( vUv.y < - 1.0 || vUv.y > 1.0 ) discard; // discard endcaps

				if ( mod( vLineDistance + dashOffset, dashSize + gapSize ) > dashSize ) discard; // todo - FIX

			#endif

			#ifdef WORLD_UNITS

				// Find the closest points on the view ray and the line segment
				vec3 rayEnd = normalize( worldPos.xyz ) * 1e5;
				vec3 lineDir = worldEnd - worldStart;
				vec2 params = closestLineToLine( worldStart, worldEnd, vec3( 0.0, 0.0, 0.0 ), rayEnd );

				vec3 p1 = worldStart + lineDir * params.x;
				vec3 p2 = rayEnd * params.y;
				vec3 delta = p1 - p2;
				float len = length( delta );
				float norm = len / linewidth;

				#ifndef USE_DASH

					#ifdef USE_ALPHA_TO_COVERAGE

						float dnorm = fwidth( norm );
						alpha = 1.0 - smoothstep( 0.5 - dnorm, 0.5 + dnorm, norm );

					#else

						if ( norm > 0.5 ) {

							discard;

						}

					#endif

				#endif

			#else

				#ifdef USE_ALPHA_TO_COVERAGE

					// artifacts appear on some hardware if a derivative is taken within a conditional
					float a = vUv.x;
					float b = ( vUv.y > 0.0 ) ? vUv.y - 1.0 : vUv.y + 1.0;
					float len2 = a * a + b * b;
					float dlen = fwidth( len2 );

					if ( abs( vUv.y ) > 1.0 ) {

						alpha = 1.0 - smoothstep( 1.0 - dlen, 1.0 + dlen, len2 );

					}

				#else

					if ( abs( vUv.y ) > 1.0 ) {

						float a = vUv.x;
						float b = ( vUv.y > 0.0 ) ? vUv.y - 1.0 : vUv.y + 1.0;
						float len2 = a * a + b * b;

						if ( len2 > 1.0 ) discard;

					}

				#endif

			#endif

			#include <logdepthbuf_fragment>
			#include <color_fragment>

			gl_FragColor = vec4( diffuseColor.rgb, alpha );

			#include <tonemapping_fragment>
			#include <colorspace_fragment>
			#include <fog_fragment>
			#include <premultiplied_alpha_fragment>

		}
		`};var X=class extends xt{constructor(n){super({type:"LineMaterial",uniforms:Re.clone(de.line.uniforms),vertexShader:de.line.vertexShader,fragmentShader:de.line.fragmentShader,clipping:!0}),this.isLineMaterial=!0,this.setValues(n)}get color(){return this.uniforms.diffuse.value}set color(n){this.uniforms.diffuse.value=n}get worldUnits(){return"WORLD_UNITS"in this.defines}set worldUnits(n){n===!0?this.defines.WORLD_UNITS="":delete this.defines.WORLD_UNITS}get linewidth(){return this.uniforms.linewidth.value}set linewidth(n){this.uniforms.linewidth&&(this.uniforms.linewidth.value=n)}get dashed(){return"USE_DASH"in this.defines}set dashed(n){n===!0!==this.dashed&&(this.needsUpdate=!0),n===!0?this.defines.USE_DASH="":delete this.defines.USE_DASH}get dashScale(){return this.uniforms.dashScale.value}set dashScale(n){this.uniforms.dashScale.value=n}get dashSize(){return this.uniforms.dashSize.value}set dashSize(n){this.uniforms.dashSize.value=n}get dashOffset(){return this.uniforms.dashOffset.value}set dashOffset(n){this.uniforms.dashOffset.value=n}get gapSize(){return this.uniforms.gapSize.value}set gapSize(n){this.uniforms.gapSize.value=n}get opacity(){return this.uniforms.opacity.value}set opacity(n){this.uniforms&&(this.uniforms.opacity.value=n)}get resolution(){return this.uniforms.resolution.value}set resolution(n){this.uniforms.resolution.value.copy(n)}get alphaToCoverage(){return"USE_ALPHA_TO_COVERAGE"in this.defines}set alphaToCoverage(n){this.defines&&(n===!0!==this.alphaToCoverage&&(this.needsUpdate=!0),n===!0?this.defines.USE_ALPHA_TO_COVERAGE="":delete this.defines.USE_ALPHA_TO_COVERAGE)}};var Ge=new G,Ft=new b,zt=new b,p=new G,g=new G,S=new G,Qe=new b,$e=new vt,_=new St,Ut=new b,we=new re,Se=new me,C=new G,T,K;function Rt(r,n,e){return C.set(0,0,-n,1).applyMatrix4(r.projectionMatrix),C.multiplyScalar(1/C.w),C.x=K/e.width,C.y=K/e.height,C.applyMatrix4(r.projectionMatrixInverse),C.multiplyScalar(1/C.w),Math.abs(Math.max(C.x,C.y))}function Xt(r,n){let e=r.matrixWorld,i=r.geometry,t=i.attributes.instanceStart,s=i.attributes.instanceEnd,o=Math.min(i.instanceCount,t.count);for(let a=0,d=o;a<d;a++){_.start.fromBufferAttribute(t,a),_.end.fromBufferAttribute(s,a),_.applyMatrix4(e);let l=new b,h=new b;T.distanceSqToSegment(_.start,_.end,h,l),h.distanceTo(l)<K*.5&&n.push({point:h,pointOnLine:l,distance:T.origin.distanceTo(h),object:r,face:null,faceIndex:a,uv:null,uv1:null})}}function Yt(r,n,e){let i=n.projectionMatrix,s=r.material.resolution,o=r.matrixWorld,a=r.geometry,d=a.attributes.instanceStart,l=a.attributes.instanceEnd,h=Math.min(a.instanceCount,d.count),u=-n.near;T.at(1,S),S.w=1,S.applyMatrix4(n.matrixWorldInverse),S.applyMatrix4(i),S.multiplyScalar(1/S.w),S.x*=s.x/2,S.y*=s.y/2,S.z=0,Qe.copy(S),$e.multiplyMatrices(n.matrixWorldInverse,o);for(let E=0,Kt=h;E<Kt;E++){if(p.fromBufferAttribute(d,E),g.fromBufferAttribute(l,E),p.w=1,g.w=1,p.applyMatrix4($e),g.applyMatrix4($e),p.z>u&&g.z>u)continue;if(p.z>u){let V=p.z-g.z,L=(p.z-u)/V;p.lerp(g,L)}else if(g.z>u){let V=g.z-p.z,L=(g.z-u)/V;g.lerp(p,L)}p.applyMatrix4(i),g.applyMatrix4(i),p.multiplyScalar(1/p.w),g.multiplyScalar(1/g.w),p.x*=s.x/2,p.y*=s.y/2,g.x*=s.x/2,g.y*=s.y/2,_.start.copy(p),_.start.z=0,_.end.copy(g),_.end.z=0;let qe=_.closestPointToPointParameter(Qe,!0);_.at(qe,Ut);let Xe=_t.lerp(p.z,g.z,qe),Vt=Xe>=-1&&Xe<=1,Ht=Qe.distanceTo(Ut)<K*.5;if(Vt&&Ht){_.start.fromBufferAttribute(d,E),_.end.fromBufferAttribute(l,E),_.start.applyMatrix4(o),_.end.applyMatrix4(o);let V=new b,L=new b;T.distanceSqToSegment(_.start,_.end,L,V),e.push({point:L,pointOnLine:V,distance:T.origin.distanceTo(L),object:r,face:null,faceIndex:E,uv:null,uv1:null})}}}var Ce=class extends Q{constructor(n=new q,e=new X({color:Math.random()*16777215})){super(n,e),this.isLineSegments2=!0,this.type="LineSegments2"}computeLineDistances(){let n=this.geometry,e=n.attributes.instanceStart,i=n.attributes.instanceEnd,t=new Float32Array(2*e.count);for(let o=0,a=0,d=e.count;o<d;o++,a+=2)Ft.fromBufferAttribute(e,o),zt.fromBufferAttribute(i,o),t[a]=a===0?0:t[a-1],t[a+1]=t[a]+Ft.distanceTo(zt);let s=new oe(t,2,1);return n.setAttribute("instanceDistanceStart",new B(s,1,0)),n.setAttribute("instanceDistanceEnd",new B(s,1,1)),this}raycast(n,e){let i=this.material.worldUnits,t=n.camera;t===null&&!i&&console.error('LineSegments2: "Raycaster.camera" needs to be set in order to raycast against LineSegments2 while worldUnits is set to false.');let s=n.params.Line2!==void 0&&n.params.Line2.threshold||0;T=n.ray;let o=this.matrixWorld,a=this.geometry,d=this.material;K=d.linewidth+s,a.boundingSphere===null&&a.computeBoundingSphere(),Se.copy(a.boundingSphere).applyMatrix4(o);let l;if(i)l=K*.5;else{let u=Math.max(t.near,Se.distanceToPoint(T.origin));l=Rt(t,u,d.resolution)}if(Se.radius+=l,T.intersectsSphere(Se)===!1)return;a.boundingBox===null&&a.computeBoundingBox(),we.copy(a.boundingBox).applyMatrix4(o);let h;if(i)h=K*.5;else{let u=Math.max(t.near,we.distanceToPoint(T.origin));h=Rt(t,u,d.resolution)}we.expandByScalar(h),T.intersectsBox(we)!==!1&&(i?Xt(this,e):Yt(this,t,e))}onBeforeRender(n){let e=this.material.uniforms;e&&e.resolution&&(n.getViewport(Ge),this.material.uniforms.resolution.value.set(Ge.z,Ge.w))}};var Te=class extends q{constructor(){super(),this.isLineGeometry=!0,this.type="LineGeometry"}setPositions(n){let e=n.length-3,i=new Float32Array(2*e);for(let t=0;t<e;t+=3)i[2*t]=n[t],i[2*t+1]=n[t+1],i[2*t+2]=n[t+2],i[2*t+3]=n[t+3],i[2*t+4]=n[t+4],i[2*t+5]=n[t+5];return super.setPositions(i),this}setColors(n){let e=n.length-3,i=new Float32Array(2*e);for(let t=0;t<e;t+=3)i[2*t]=n[t],i[2*t+1]=n[t+1],i[2*t+2]=n[t+2],i[2*t+3]=n[t+3],i[2*t+4]=n[t+4],i[2*t+5]=n[t+5];return super.setColors(i),this}setFromPoints(n){let e=n.length-1,i=new Float32Array(6*e);for(let t=0;t<e;t++)i[6*t]=n[t].x,i[6*t+1]=n[t].y,i[6*t+2]=n[t].z||0,i[6*t+3]=n[t+1].x,i[6*t+4]=n[t+1].y,i[6*t+5]=n[t+1].z||0;return super.setPositions(i),this}fromLine(n){let e=n.geometry;return this.setPositions(e.attributes.position.array),this}};var Me=class extends Ce{constructor(n=new Te,e=new X({color:Math.random()*16777215})){super(n,e),this.isLine2=!0,this.type="Line2"}};function Jt(r,n){if(r&1){let e=Le();m(0,"mat-tree-node",6),v("mouseenter",function(){let t=P(e).$implicit,s=M();return O(s.onMouseEnterNode(t))})("mouseleave",function(){let t=P(e).$implicit,s=M();return O(s.onMouseLeaveNode(t))}),at(1,"button",7),A(2),m(3,"button",8),v("click",function(){let t=P(e).$implicit,s=M();return O(s.toggleVisibility(t))}),m(4,"mat-icon"),A(5),z()()()}if(r&2){let e=n.$implicit,i=M();Pe("event-track-node",i.isTrackNode(e)),w(2),ge(" ",e.name," "),w(3),pe(i.isEffectivelyVisible(e.object3D)?"visibility":"visibility_off")}}function Zt(r,n){if(r&1){let e=Le();m(0,"mat-tree-node",6),v("mouseenter",function(){let t=P(e).$implicit,s=M();return O(s.onMouseEnterNode(t))})("mouseleave",function(){let t=P(e).$implicit,s=M();return O(s.onMouseLeaveNode(t))}),m(1,"button",9)(2,"mat-icon",10),A(3),z()(),A(4),m(5,"button",8),v("click",function(){let t=P(e).$implicit,s=M();return O(s.toggleVisibility(t))}),m(6,"mat-icon"),A(7),z()()()}if(r&2){let e=n.$implicit,i=M();Pe("event-track-node",i.isTrackNode(e)),w(),j("aria-label","Toggle "+e.name),w(2),ge(" ",i.treeControl.isExpanded(e)?"expand_more":"chevron_right"," "),w(),ge(" ",e.name," "),w(3),pe(i.isEffectivelyVisible(e.object3D)?"visibility":"visibility_off")}}var fn=(()=>{let n=class n{constructor(i){this.threeService=i,this.configureItem=new ie,this.isHighlightingEnabled=!1,this.isTrackHighlightingEnabled=!1,this.geometryHighlightMaterial=new yt({color:16776960,wireframe:!0}),this.treeControl=new ve(t=>t.level,t=>t.expandable),this.treeFlattener=new be((t,s)=>({expandable:!!t.children&&t.children.length>0,name:t.name||"(untitled)",level:s,type:t.type,object3D:t,visible:t.visible}),t=>t.level,t=>t.expandable,t=>t.children),this.dataSource=new Ee(this.treeControl,this.treeFlattener),this.hasChild=(t,s)=>s.expandable}ngOnInit(){this.refreshSceneTree()}get isAnyHighlightingEnabled(){return this.isHighlightingEnabled||this.isTrackHighlightingEnabled}toggleHighlighting(){let i=!this.isAnyHighlightingEnabled;this.isHighlightingEnabled=i,this.isTrackHighlightingEnabled=i}refreshSceneTree(){this.dataSource.data=[];let i=this.threeService.scene;if(!i){console.warn("No scene present in ThreeService.");return}this.dataSource.data=i.children,this.treeControl.collapseAll()}isEffectivelyVisible(i){let t=i;for(;t;){if(!t.visible)return!1;t=t.parent}return!0}revealPath(i,t=!1){let s=i,o=s.parent;for(;o;)o.visible||(o.visible=!0,o.children.forEach(a=>{a!==s&&(a.visible=!1)})),s=o,o=o.parent;t&&i.traverse(a=>a.visible=!0)}toggleVisibility(i){let t=i.object3D;t.visible?t.visible=!1:(()=>{for(let o=t.parent;o;o=o.parent)if(!o.visible)return!0;return!1})()?(this.revealPath(t,!1),t.visible=!0):(this.revealPath(t,!0),t.visible=!0),i.visible=this.isEffectivelyVisible(t)}onMouseEnterNode(i){this.isHighlightingEnabled&&!this.isTrackNode(i)&&this.highlightNode(i),this.isTrackHighlightingEnabled&&this.isTrackNode(i)&&this.highlightTrack(i)}onMouseLeaveNode(i){this.isHighlightingEnabled&&!this.isTrackNode(i)&&this.unhighlightNode(i),this.isTrackHighlightingEnabled&&this.isTrackNode(i)&&this.unhighlightTrack(i)}highlightNode(i){i.object3D.traverse(t=>{t instanceof Q&&(t.userData.origMaterial||(t.userData.origMaterial=t.material),t.material=this.geometryHighlightMaterial)})}unhighlightNode(i){i.object3D.traverse(t=>{t instanceof Q&&t.userData.origMaterial&&(t.material=t.userData.origMaterial,delete t.userData.origMaterial)})}isTrackNode(i){return this.isUnderEventParent(i)&&(i.name.toLowerCase().includes("track")||this.hasLineGeometry(i.object3D)||i.object3D.userData?.isTrack===!0)}isUnderEventParent(i){if(i.name.toLowerCase()==="event"||i.object3D.userData?.isEvent===!0)return!0;let t=i.object3D;for(;t&&t.parent;){if(t.parent.name.toLowerCase()==="event"||t.parent.userData?.isEvent===!0)return!0;t=t.parent}return!1}hasLineGeometry(i){let t=!1;return i.traverse(s=>{(s instanceof bt||s instanceof Et||s instanceof Me||s instanceof Q&&s.geometry&&s.geometry.type.includes("Line"))&&(t=!0)}),t}highlightTrack(i){i.object3D.traverse(t=>{t.userData.highlightFunction&&t.userData.highlightFunction()})}unhighlightTrack(i){i.object3D.traverse(t=>{t.userData.unhighlightFunction&&t.userData.unhighlightFunction()})}};n.\u0275fac=function(t){return new(t||n)(rt(Ct))},n.\u0275cmp=H({type:n,selectors:[["app-scene-tree"]],outputs:{configureItem:"configureItem"},decls:10,vars:4,consts:[[1,"header"],["mat-icon-button","","aria-label","Toggle Highlights","matTooltip","Toggle  highlights",1,"button_theme",3,"click"],["mat-icon-button","","aria-label","Refresh","matTooltip","Refresh tree with current geometry",1,"button_theme",3,"click"],[3,"dataSource","treeControl"],["matTreeNodePadding","",3,"event-track-node","mouseenter","mouseleave",4,"matTreeNodeDef"],["matTreeNodePadding","",3,"event-track-node","mouseenter","mouseleave",4,"matTreeNodeDef","matTreeNodeDefWhen"],["matTreeNodePadding","",3,"mouseenter","mouseleave"],["mat-icon-button","","disabled",""],["mat-icon-button","",3,"click"],["mat-icon-button","","matTreeNodeToggle",""],[1,"mat-icon-rtl-mirror"]],template:function(t,s){t&1&&(m(0,"div",0)(1,"button",1),v("click",function(){return s.toggleHighlighting()}),m(2,"mat-icon"),A(3),z()(),m(4,"button",2),v("click",function(){return s.refreshSceneTree()}),m(5,"mat-icon"),A(6,"refresh"),z()()(),m(7,"mat-tree",3),ot(8,Jt,6,4,"mat-tree-node",4)(9,Zt,8,6,"mat-tree-node",5),z()),t&2&&(w(3),pe(s.isAnyHighlightingEnabled?"highlight_off":"highlight"),w(4),Be("dataSource",s.dataSource)("treeControl",s.treeControl),w(2),Be("matTreeNodeDefWhen",s.hasChild))},dependencies:[Lt,At,Pt,It,Bt,gt,Tt,pt],styles:[".header[_ngcontent-%COMP%]{display:flex;justify-content:flex-end}.header[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]{width:48px;height:48px;min-width:48px;padding-top:8px}.button_theme[_ngcontent-%COMP%]{background-color:var(--background-color);color:var(--text-color);transition:background-color .3s,color .3s}.button_theme[_ngcontent-%COMP%]:hover{background-color:var(--secondary-background-color);color:var(--accent-color)}.mat-tree[_ngcontent-%COMP%]{background-color:transparent!important}"]});let r=n;return r})();export{X as a,Te as b,Me as c,fn as d};
