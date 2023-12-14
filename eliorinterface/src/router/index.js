import Vue from 'vue';
import Router from 'vue-router';
import DocumentUpload from '@/components/DocumentUpload';
import DataEntryForm from '@/components/DataEntryForm';
import SearchComponent from '@/components/SearchComponent';
import WordListComponent from '@/components/WordListComponent';
import WordContext from '@/components/WordContext';
import WordIndex from '@/components/WordIndex';
import LocationSearch from '@/components/LocationSearch';
import WordGroups from '@/components/WordGroups';
import LinguisticExpressions from '@/components/LinguisticExpressions';
import StatisticsDisplay from '@/components/StatisticsDisplay';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'DocumentUpload',
            component: DocumentUpload
        },
        {
            path: '/data-entry',
            name: 'DataEntryForm',
            component: DataEntryForm
        },
        {
            path: '/search',
            name: 'SearchComponent',
            component: SearchComponent
        },
        {
            path: '/words',
            name: 'WordList',
            component: WordListComponent
        },
        {
            path: '/word-context',
            name: 'WordContext',
            component: WordContext
        },
        {
            path: '/word-index',
            name: 'WordIndex',
            component: WordIndex
        },
        {
            path: '/location-search',
            name: 'LocationSearch',
            component: LocationSearch
        },
        {
            path: '/word-groups',
            name: 'WordGroups',
            component: WordGroups
        },
        {
            path: '/linguistic-expressions',
            name: 'LinguisticExpressions',
            component: LinguisticExpressions
        },
        {
            path: '/statistics',
            name: 'StatisticsDisplay',
            component: StatisticsDisplay
        }

    ]
});
